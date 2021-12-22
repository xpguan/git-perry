import netaddr
import bisect
import json
from multiprocessing import Pool as mp
import copy
result = []



def aggregate_itepremium(v_subnet):
    result = []
    v_subnet_c = copy.deepcopy(v_subnet)
    if v_subnet[0] != "0.0.0.0/0":
        for item in v_subnet:
            bigger_item =item
            item_result = []
            ranges = []
            for item2 in v_subnet_c:
                if item2 == item:
                    continue
                if item[1] == item2[1]:
                    ranges = [netaddr.IPNetwork(bigger_item[0]).first, netaddr.IPNetwork(bigger_item[0]).last]                
                    subnet = netaddr.IPNetwork(item2[0])
                    first = bisect.bisect_left(ranges, subnet.first)
                    last = bisect.bisect_right(ranges, subnet.last)
                    if first == last and first == 1:
                        continue
                    if first == 0 and last == 2 :
                        bigger_item = item2
                    else:
                        continue     
                # print(item[0] + ": " + bigger_item[0] + ": " + item2[0] + ":" + str(first) + " "+ str(last))
                else:
                    continue

            if bigger_item not in result and bigger_item:
                print(bigger_item)
                result.append(bigger_item)
                with open("aggregate_vrf_result.txt","a") as f:
                    str_result_item = str(bigger_item) + "\n"
                    f.write(str(str_result_item))
    with open("aggregate_result.json","w") as f:
                json.dump(result,f)


with open("test.json", "r") as f:
    itepremium = json.load(f)


aggregate_itepremium(itepremium)

# pool = mp(20)
# pool.map(aggregate_itepremium, itepremium)
# pool.close()
# pool.join()