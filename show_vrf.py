import json 

with open("itepremium_china.json","r") as f: 
    data2 = json.load(f)

route_as_path = []
for item in data2['route-information'][0]['route-table'][0]['rt']:
    as_path =""
    route_item = []
    if 'as-path' in item['rt-entry'][0]:
        as_path = item['rt-entry'][0]['as-path'][0]['data']
    route = item['rt-destination'][0]['data']
    route_item.append(route)
    route_item.append(as_path)
    route_as_path.append(route_item)

with open("vrf_active_china.json","w") as f:
    json.dump(route_as_path,f)

print ("ok")