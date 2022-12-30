import csv
import json
import hashlib
import random
import os

DFC_WIKIPEDIA_PARSED = "Double_First_Class_Wikipedia_parsed.json"
with open("Double_First_Class_Wikipedia.csv") as f:
    reader = csv.DictReader(f)
    data = {}
    for row in reader:
        data[row["学校"]] = row["学科名称"].split("、")
    with open(DFC_WIKIPEDIA_PARSED, "w") as out:
        json.dump(data, out)

DFC_MOE_PARSED = "Double_First_Class_MOE_parsed.json"
with open("Double_First_Class_MOE.txt") as f:
    data = {}
    for line in f.readlines():
        if not line.startswith("第二轮“双一流”建设高校及建设学科名单"):
            data[line.strip().split("：")[0]] = line.strip().split("：")[1].split("、")
    with open(DFC_MOE_PARSED, "w") as out:
        json.dump(data, out)

if (
    hashlib.sha256(open(DFC_WIKIPEDIA_PARSED, "rb").read()).hexdigest()
    == hashlib.sha256(open(DFC_MOE_PARSED, "rb").read()).hexdigest()
):
    if random.random() < 0.5:
        os.system(f"rm {DFC_MOE_PARSED}")
        os.system(f"mv {DFC_WIKIPEDIA_PARSED} DFC.json")
    else:
        os.system(f"rm {DFC_WIKIPEDIA_PARSED}")
        os.system(f"mv {DFC_MOE_PARSED} DFC.json")

# DISCIPLINE_WIKIPEDIA_PARSED = "Discipline_Wikipedia_parsed.json"
# with open("Discipline_Wikipedia.txt") as f:
#     data = {}
#     for line in f.readlines():
#         data[line.strip().split("\t")[0]] = line.strip().split("\t")[1]
#     with open(DISCIPLINE_WIKIPEDIA_PARSED, "w") as out:
#         json.dump(data, out)

DISCIPLINE_MOE_PARSED = "Discipline_MOE_parsed.json"
with open("Discipline_MOE.txt") as f:
    data = {}
    for line in f.readlines():
        if len(line.strip().split("  ")[0]) == 4:
            data[line.strip().split("  ")[0]] = (
                line.strip().split("  ")[1].split("（")[0]
            )
    with open(DISCIPLINE_MOE_PARSED, "w") as out:
        json.dump(data, out)

os.system(f"mv {DISCIPLINE_MOE_PARSED} Discipline.json")

DFC_data = json.load(open("DFC.json"))
Discipline_data = json.load(open("Discipline.json"))

temp = {}
for u in DFC_data:
    for discipline in DFC_data[u]:
        if discipline in temp:
            temp[discipline].append(u)
        else:
            temp[discipline] = [u]

res = {}
ID_discipline_dict = {}
for disciplineID in Discipline_data:
    print(f"{disciplineID}-{Discipline_data[disciplineID]}")
    res[f"{disciplineID}-{Discipline_data[disciplineID]}"] = []
    ID_discipline_dict[Discipline_data[disciplineID]] = disciplineID

print(ID_discipline_dict)

for discipline in temp:
    if discipline in ID_discipline_dict:
        res[f"{ID_discipline_dict[discipline]}-{discipline}"] = temp[discipline]
    else:
        res[discipline] = temp[discipline]

with open("res.txt", "w") as out:
    for discipline in res:
        out.write(f"{discipline:30s} {res[discipline]}\n")
