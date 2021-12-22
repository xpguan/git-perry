import netaddr
import bisect
import json
from multiprocessing import Pool as mp
result = []

def subnets_overlap(v_subnet):
    # ranges will be a sorted list of alternating start and end addresses

    if v_subnet[0] != "0.0.0.0/0":
        for g_subnet in inet0:
            if g_subnet[0] == "0.0.0.0/0":
                continue
            else:
                result_item = {'itepremium':{'route':"",'as-path':""},'inet0':{'route':"",'as-path':""}}
                ranges = []
                subnets = [netaddr.IPNetwork(g_subnet[0]), netaddr.IPNetwork(v_subnet[0])]
                for subnet in subnets:
                    # find indices to insert start and end addresses
                    first = bisect.bisect_left(ranges, subnet.first)
                    last = bisect.bisect_right(ranges, subnet.last)
                    # check the overlap conditions and return if one is met
                    if first != last or first % 2 == 1:
                        result_item['itepremium']['route'] = v_subnet[0]
                        result_item['itepremium']['as-path'] = v_subnet[1]
                        result_item['inet0']['route'] = g_subnet[0]
                        result_item['inet0']['as-path'] = g_subnet[1]
                        result.append(result_item)
                        print(result_item)
                        with open("result.txt","a") as f:
                            str_result_item = str(result_item) + "\n"
                            f.write(str(str_result_item))
                    ranges[first:first] = [subnet.first, subnet.last]
            

def aggregate_itepremium(v_subnet):
    result = []
    if v_subnet[0] != "0.0.0.0/0":
        for i in range(len(v_subnet)):
            item = v_subnet[i]
            v_subnet.pop(i)
            item_result = []
            for item2 in v_subnet:
                if not item_result:
                    item_result = item
                ranges = []
                subnets = [netaddr.IPNetwork(item_result), netaddr.IPNetwork(item2)]
                for subnet in subnets:
                    # find indices to insert start and end addresses
                    first = bisect.bisect_left(ranges, subnet.first)
                    last = bisect.bisect_right(ranges, subnet.last)
                    # check the overlap conditions and return if one is met
                    if first == last == 1 and item[1] == item2[1]:
                        item_result = item
                        v_subnet.remove(item2)
                    if first == 0 and last == 2 and item[1] == item2[1]:
                        item_result = item2
            result.append(item_result)
    return(result)




with open("inet.0_active-full.json","r") as f:
    inet0 = json.load(f)['Rows']
with open("vrf_active.json", "r") as f:
    itepremium = json.load(f)


pool = mp(20)
pool.map(subnets_overlap, itepremium)
pool.close()
pool.join()




with open("result.json","w") as f:
    json.dump(result,f)

                    # print(subnet[0] + " : " + subnet[1] + " | " +  g_subnet[0] + " : " + g_subnet[1] +  " have overlapping")




