def gen_service_app(rule_id, service, dst_port, protocol):

	### Make lowercase
	protocol = normalize_protocol(protocol)

	app_name = protocol + "-" + dst_port

	config1 = "set applications application " 
	config2 = " protocol "
	config3 = " destination-port "
	config4 = " description "

	#final_config = config1 + app_name + config2 + protocol + config3 + dst_port + config4 + "'" +rule_id+ "'"
	final_config = config1 + app_name + config2 + protocol + config3 + dst_port 

	print final_config
	
	### Return app name ready to be added to list

	return app_name

def normalize_protocol(protocol):

	protocol = protocol.decode('utf-8').lower()

	return protocol