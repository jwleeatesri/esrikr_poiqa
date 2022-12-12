"""
Processes the POI data and finds accuracy ratio
"""
from collections import Counter
from datetime import datetime
import json
import logging
import os
import pandas as pd
# from googletrans import Translator; tr = Translator()
from konlpy.tag import Komoran

# local imports
from settings import BUILD_CSV
from enums import Category, Subcategory

__version__ = "0.2.0"

# start komoran
komoran = Komoran()

# PATHS
OUTPUT_DIR = os.path.join(os.getcwd(),"prepare")
LOG_DIR = os.path.join(os.getcwd(), "logs")
REPORTS_DIR = os.path.join(os.getcwd(),"reports")

# logging config
logging.basicConfig(filename=os.path.join(LOG_DIR,"debug.log"),level=logging.DEBUG)

def get_common_words(_df:pd.DataFrame,
                    category: Category,
                    num=100) -> None:
    """Get common names from the dataframe
    :param df: Dataframe
    :param category Category: category
    :param num int: number of points"""
    df_interest_name = _df.loc[_df["category"] == category.value].name
    prep_list = []
    for elem in df_interest_name:
        prep_list += komoran.nouns(elem)
    commons = Counter(prep_list).most_common(num)
    if len(commons) < num:
        logging.warning("%s The commons list has less than %s elements.\
        len(%s) = %s",
        datetime.now(),
        num,
        category.value,
        len(commons))

    output_filename = os.path.join(OUTPUT_DIR,f"Category_{category.value.replace(' ','_')}.csv")
    with open(output_filename,"w",encoding="utf-8") as _f:
        _f.write("kor,eng,priority,warn\n")
        for item in commons:
            if len(value:=item[0].strip()) > 1:
                _f.write(f"{value},\n")

    logging.info('%s %s created.', datetime.now(), output_filename)

def get_common_words_sub(_df: pd.DataFrame,
                        subcategory: Subcategory,
                        num=20) -> None:
    """Get common names from the dataframe
    :param df: Dataframe
    :param subcategory Subcategory: subcategory
    :param num int: number of points"""
    df_interest_name = _df.loc[_df["subcategory"] == subcategory.value].name
    prep_list = []
    for elem in df_interest_name:
        prep_list += komoran.nouns(elem)
    commons = Counter(prep_list).most_common(num)
    if (comlen:=len(commons)) == 0:
        logging.warning("%s The commons list has 0 elements. No file is created for %s",\
            datetime.now(),\
            subcategory.value)
        return
    if comlen < num:
        logging.warning("%s The commons list has less than %s elements.\
        len(%s) = %s",
        datetime.now(),
        num,
        subcategory.value,
        len(commons))

    output_filename = os.path.join(OUTPUT_DIR,\
        f"Subcategory_{subcategory.value.replace(' ','_')}.csv")
    with open(output_filename,"w",encoding="utf-8") as _f:
        _f.write("kor,eng,priority,warn\n")
        for item in commons:
            if len(value:=item[0].strip()) > 1:
                _f.write(f"{value},,,\n")

    logging.info('%s %s created.', datetime.now(), output_filename)

def build_all_prep_csvs(_df:pd.DataFrame, sub=True):
    """Iterate through all of the category
    :param df: the df to scrap
    """
    if sub:
        for _, subcategory in Subcategory.__members__.items():
            get_common_words_sub(_df,subcategory)
    else:
        for _, category in Category.__members__.items():
            get_common_words(_df,category)
    logging.info("%s Built all prep csvs", datetime.now())

def load_location_dictionary() -> dict:
    """Read the regions.json file and load the location dictionary"""
    json_source = os.path.join(os.getcwd(), "regions.json")
    with open(json_source,"r",encoding="utf-8") as _f:
        data = json.loads(_f.read())
    return data

def update_json(category:str,
                subcategory:Subcategory,
                correct:int,
                incorrect:int):
    """Use the given values to update the json file"""
    update_path = os.path.join(REPORTS_DIR, category,"report.json")
    with open(update_path, "r", encoding="utf-8") as f:
        data:dict = json.load(f)
        data[subcategory.value]["incorrect"] = incorrect
        data[subcategory.value]["correct"] = correct
    result_json = json.dumps(data)
    with open(update_path, "w", encoding="utf-8") as p:
        print("Im in!")
        p.write(result_json)
        print("Im out!")


def process_by_subcategory(_df: pd.DataFrame, subcategory: Subcategory) -> float:
    """Read df and reviews the categories
    :param _df DataFrame: source dataframe (this dataframe is the entire dataset)
    :param subcategory Subcategory: target subcategory"""
    filename = f"Subcategory_{subcategory.value.replace(' ','_')}.csv"
    subcategory_dict_name = os.path.join(OUTPUT_DIR,filename)
    with open(subcategory_dict_name,"r",encoding="utf-8") as _f:
        data = _f.readlines()[1:]
    _dictionary = [(row.split(",")[0],row.split(",")[1]) for row in data]
    if _dictionary[0][1] == "":
        raise AttributeError("The dictionary has not yet been built")
    problems = set([])
    def review(row):
        """Apply this function to compare results
        :param row: the row to process. use axis=1 for df.apply
        """
        name = row["name"]
        name_eng = row["name_eng"].lower()
        for elem in sorted(_dictionary,key=lambda x:len(x[0])):
            if elem[0] in name and elem[1].lower() not in name_eng:
                # print(elem[1].lower(),end="\t")
                # print(name_eng)
                problems.add(elem[0])
                return False
        return True
    df_interest = _df.loc[_df["subcategory"] == subcategory.value].copy()
    df_interest.loc[:,"result"] = df_interest.apply(review,axis=1)
    df_result = df_interest.loc[df_interest["result"] == False] # deprecated?
    main_category = df_interest["category"].iloc[0]
    # if no problem, no file
    if len(problems) == 0:
        logging.info("%s No errors for the file: %s",datetime.now(),subcategory.value)
        update_json(main_category,subcategory,len(df_interest),0) 
        print(f"YAY {subcategory.value} 0 probs")
    else:
        subcategory_report_name = os.path.join(REPORTS_DIR,main_category,filename)
        df_result.to_csv(subcategory_report_name,encoding="utf-8")
        update_json(main_category,subcategory,len(df_interest) - len(df_result),len(df_result))
        print(f"YAY {subcategory.value} probs")
    return 100 * len(df_result)/len(df_interest)

def process_all(_df: pd.DataFrame):
    """Process all the subcategories at once
    and alert if the dictionary is not yet translated.
    """
    for _, member in Subcategory.__members__.items():
        try:
            process_by_subcategory(_df,member)
        except AttributeError:
            # logging.warning("%s %s dictionary is not yet built",
            #     datetime.now(),
            #     member.value)
            pass

if __name__ == "__main__":
    dw = pd.read_csv("dw_poi_all.csv", encoding="utf-8")
    location_dictionary = load_location_dictionary()
    if BUILD_CSV:
        build_all_prep_csvs(dw)
    process_all(dw)
