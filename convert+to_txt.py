import json

with open("result_aggregate.json","r") as f:
    data = json.load(f)



for i in data: 
    item = i["itepremium"]["route"] + "|" + i["itepremium"]["as-path"] + "|" + i["inet0"]["route"] + "|" + i["inet0"]["as-path"] + "\n"
    with open("final_result.txt","a") as f:
        f.write(item)



