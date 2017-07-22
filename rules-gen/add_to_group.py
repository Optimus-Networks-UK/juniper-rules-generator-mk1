def add(rule_id, host,  host_group_name):

	

	config1 = "set security address-book global address-set " 
	config2 = " address "

	### Descriptions don't work for address-set!

	final_config = config1 + host_group_name + config2 + host

	print final_config
	
	### Return config ready to be added to list

	return host

def app_set(rule_id, app, app_set):

	config1 = "set applications application-set " 
	config2 = " application "


	final_config = config1 + app_set + config2 + app 

	print final_config
	
	### Return config ready to be added to list