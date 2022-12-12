from korean_romanizer.romanizer import Romanizer
SOUTH_KOREA = {
  "all": []
}

CLASSIFIERS = [
  [("특별시","Special City","teukbyeolsi","si"),
    ("광역시","Metropolitan City", "gwangyeoksi","si"),
    ("특별자치시","Special Self-governing City","teukbyoel-jachisi","si"),
    ("도","Province","do","do"),
    ("특별자치도","Special Self-governing Province","teukbyeol-jachido","do")],
  [("시","City","si"),
    ("군","County","gun"),
    ("구","District","gu"),
    # 세종특별자치시는 예하에 시군구 대신 읍면동이 있네
    ("읍","Town","eup"),
    ("면","Township","myeon"),
    ("동","Neighborhood","dong")]]

def process_lvl_1(row):
  row = row[0].strip()
  print(row)
  if row not in SOUTH_KOREA["all"]:
    SOUTH_KOREA["all"].append(row) 
  for classifier in CLASSIFIERS[0]: # 0에 시,도 있음
    if classifier[0] in row:
      name = row.replace(classifier[0],"")
      print(f"{name}\t{len(name)}\t{type(name)}")
      SOUTH_KOREA[row] = {
        "class":classifier[0],
        "name": name,
        "name_eng": Romanizer(name).romanize().title(),
        "english_class":classifier[1],
        "roman":classifier[2],
        "short":classifier[3],
        "subregion":{
          "all":[]
        }
      }

def process_lvl_2(row):
  lvl1, lvl2 = row
  lvl1 = lvl1.strip(); lvl2 = lvl2.strip()
  # print(lvl1, end="\t")
  # print(lvl2)
  
  if lvl1 not in SOUTH_KOREA.get("all"):
    process_lvl_1([lvl1])

  SOUTH_KOREA.get(lvl1).get("subregion").get("all").append(lvl2)
  for classifier in CLASSIFIERS[1]:
    if lvl2[-1:] == classifier[0]:
      name = lvl2.replace(classifier[0], "")
      SOUTH_KOREA.get(lvl1).get("subregion")[lvl2] = {
        "class":classifier[0],
        "name": name,
        "name_eng": Romanizer(name).romanize().title(),
        "english_class":classifier[1],
        "roman":classifier[2],
        "subregion":{
          "all":[]
        }
      }
      
def process_lvl_3(row):
  lvl1, lvl2, lvl3 = [_.strip() for _ in [*row]]
  
  if lvl1 not in SOUTH_KOREA.get("all"):
    process_lvl_1([lvl1])
  
  if lvl2 not in SOUTH_KOREA.get(lvl1).get("subregion").get("all"):
    process_lvl_2([lvl1,lvl2])
  
  SOUTH_KOREA\
    .get(lvl1).get("subregion")\
    .get(lvl2).get("subregion")\
    .get("all").append(lvl3)
  
  for classifier in CLASSIFIERS[1]:
    if lvl3[-1:] == classifier[0]:
      name = lvl3.replace(classifier[0],"")
      SOUTH_KOREA.get(lvl1).get("subregion")\
        .get(lvl2).get("subregion")[lvl3] = {
          "class":classifier[0],
          "name": name,
          "name_eng": Romanizer(name).romanize().title(),
          "english_class":classifier[1],
          "roman":classifier[2],
          "subregion": {
            "all":[]
          }
      }

def process_lvl_4(row):
  lvl1,lvl2,lvl3,lvl4 = [_.strip() for _ in [*row]]

  if lvl1 not in SOUTH_KOREA.get("all"):
    process_lvl_1([lvl1])
  
  if lvl2 not in SOUTH_KOREA.get(lvl1).get("subregion").get("all"):
    process_lvl_2([lvl1,lvl2])

  if lvl3 not in SOUTH_KOREA.get(lvl1).get("subregion")\
      .get(lvl2).get("all"):
    process_lvl_3([lvl1,lvl2,lvl3])

  SOUTH_KOREA\
    .get(lvl1).get("subregion")\
    .get(lvl2).get("subregion")\
    .get(lvl3).get("subregion")\
    .get("all").append(lvl4)

  for classifier in CLASSIFIERS[1]:
    if lvl4[-1:] == classifier[0]:
      name = lvl4.replace(classifier[0], "")
      SOUTH_KOREA.get(lvl1).get("subregion")\
        .get(lvl2).get("subregion")\
        .get(lvl3).get("subregion")[lvl4] = {
          "class": classifier[0],
          "name": name,
          "name_eng": Romanizer(name).romanize().title(),
          "engish_class": classifier[1],
          "roman": classifier[2],
        }
  
  

def build_json(data):
  for row in data:
    row = row.split(" ")
    if len(row) == 1:
      process_lvl_1(row)
    elif len(row) == 2:
      process_lvl_2(row)
    elif len(row) == 3:
      process_lvl_3(row)

if __name__ == "__main__":
  filename = "regions.csv"
  with open(filename,"r",encoding="utf-8") as f:
    data = f.readlines()
  
  import json

  target_file_name = "regions.json"
  build_json(data)
  with open(target_file_name, "w", encoding="utf-8") as json_file:
    json.dump(SOUTH_KOREA, json_file, ensure_ascii=False)