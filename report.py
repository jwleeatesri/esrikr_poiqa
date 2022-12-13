"""This file is for reporting stuff only."""
import json
import os
import pandas as pd
import matplotlib.pyplot as plt

from settings import *
from enums import Category, Subcategory

BASE_REPORT_PATH = os.path.join(os.getcwd(),"reports")

def build_base_json(_df):
    """Build the general skeleton of the json file
    and we can fill it up later"""
    for _, member in Category.__members__.items():
        category_path = os.path.join(BASE_REPORT_PATH,member.value)
        # get all the sub categories in the category
        subcategories = _df[_df["category"] == member.value]["subcategory"].unique()
        _cate_dict = {k:{"correct":None,"incorrect":None} for k in subcategories}
        cate_json = json.dumps(_cate_dict)

        category_json = os.path.join(category_path, "report.json")
        with open(category_json,"w",encoding="utf-8") as f:
            f.write(cate_json)
        
def read_json(category:Category):
    category_report_path = os.path.join(BASE_REPORT_PATH, category.value, "report.json")
    with open(category_report_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def build_markdown(filepath):
    with open(os.path.join(filepath,"README.md"),"w",encoding="utf-8") as f:
        f.write(r"![image](./report.png)")

def build_individual_plot(data:dict,title:str):
    report_dict = dict.fromkeys(data.keys(),0)
    # report_dict["Correct"] = 0
    fig,ax = plt.subplots()
    for k,v in data.items():
        try:
            # report_dict["Correct"] += v["correct"]
            report_dict[k] += v["incorrect"]
        except TypeError:
            pass
    try:
        filepath = os.path.join(BASE_REPORT_PATH,title,"report")
        for_md = os.path.join(BASE_REPORT_PATH,title)
        axes = sorted([(k,v) for k,v in report_dict.items()], key=lambda x:x[1])
        x_axis = [elem[1] for elem in axes]
        y_axis = [elem[0] for elem in axes]
        ax.barh(y_axis,x_axis)
        ax.set_title(title)
        ax.set_ylabel("Subcategory")
        ax.set_xlabel("Count")
        fig.savefig(filepath)
        plt.close(fig)
        build_markdown(for_md)
    except ValueError:
        pass

def build_reports():
    for _, category in Category.__members__.items():
        data = read_json(category)
        build_individual_plot(data,category.value)

if __name__ == "__main__":
    dw = pd.read_csv("dw_poi_all.csv",encoding="utf-8")
    if BUILD_BASE_JSON:
        build_base_json(dw)
    build_reports()