import logging
import json
from jnpr.junos.utils.config import Config
from lxml import etree
def Main(input, dev):
  cu = Config(dev)
  logging.info(json.dumps(input))
  filter = '<configuration><interfaces/></configuration>'
  data = dev.rpc.get_config(filter_xml=filter,options={'format':'json'})##get the running interface config from the device with json format
  config_list = []
  disabled_interfaces = []
  ## put the ae interface with "disable" but without "unit" into a list, create config with the ae interface name
  for i in data['configuration']['interfaces']['interface']:
    if ("ae" in i['name']) and ("disable" in i.keys()) and ("unit" not in i.keys()): 
	  disabled_interfaces.append(i['name'])
	  config_list.append("delete interfaces {0} disable".format(i['name']))
  config_str = "\n".join(config_list)
  if len(config_str):
	  cross_check = True
	  print("checking admin status of the interfaces:")
	  ## get the interface admin status to cross check, if the status is not "down", break and return False 
	  for i in disabled_interfaces:
		int_status = dev.rpc.get_interface_information({'format':'json'},interface_name=i, terse=True)['interface-information'][0]['physical-interface'][0]['admin-status'][0]['data']
		print( i + " : " + int_status)
		if int_status != "down":
		  cross_check = False
		  print("there is some discrepancy between interfaces config of {0} and interfaces status".format(i))
		  break
	  ##if cross check succeded , push the config to the device  
	  if cross_check:
		config_load =cu.load(config_str,format='set')
		print (etree.tostring(config_load, encoding='unicode', pretty_print=True))
		print("Config diff:")
		print(cu.pdiff())
		commit_result = cu.commit(timeout=30)
		print ("Commit Succeeded: " + str(commit_result))
		return commit_result
	  else: 
		  return False  
  else:
	  print("there is no empty disabled ae interface on this device")
	  return True