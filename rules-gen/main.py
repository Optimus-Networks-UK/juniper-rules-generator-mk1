import pymongo
import pprint

### import my other modules

import add_to_group 
import gen_group_name
import policy
import gen_app


def connect_db():

	client = pymongo.MongoClient("mongodb://admin:Thespiandelights862@10.55.88.211/admin")
	db = client['hre-import-1']

	collection = db['firewall-rules-in']

	return collection

def get_rule_by_id(collection, rule_id, source_zone, destination_zone, source_group_name, destination_group_name, application_set_name, policy_name):
   
    ### Get Source hostnames and Source IP's matching single rule ID
	snippet = collection.find({"ruleid" : rule_id})


	### Create the source group name but only if it doesn't exist yet.
	if not source_group_name:

		for i in snippet:
			### Check for presence of "Any"
			if i['Source server FQDN'] == "any":
				source_group_name = "any"
				## now exit
				
				break
			elif i['Source server FQDN'] == "Any":
				source_group_name = "any"
				## now exit
				
				break
			elif i['Source server FQDN'] == "ANY":
				source_group_name = "any"
				## now exit

				break


			### Create Group Name for source hosts
			if i['Destination server FQDN']:
				dest_host = i['Destination server FQDN']
				source_host = i['Source server FQDN']

				source_group_name = gen_group_name.src_group(dest_host, source_host)
				#print source_group_name



	### Reset Dataset snippet For Source Address creation
	snippet = collection.find({"ruleid" : rule_id})

	### Do Source Addresses

	print "#####  SOURCE ADDRESSES #####"
	
	for i in snippet:

		### Check if "any"
		if source_group_name == "any":
			break

		if i['Source server FQDN'] or i['Source IP address']:
			#print i['Source server FQDN'] + " " + i['Source IP address']


			### ToDo Juniper Code to generate source hosts

			host = i['Source server FQDN']
			ip = i['Source IP address']
			host = gen_host(rule_id, host, ip)


			###  Juniper Code to add source hosts to security groups / Address sets

			add_to_group.add(rule_id, host, source_group_name)

			#source_group.append(host)


	### Create the destination group name but only if it doesn't exist yet.

	snippet = collection.find({"ruleid" : rule_id})

	if not destination_group_name:

		for i in snippet:

			### Check for presence of "Any"
			if i['Destination server FQDN'] == "any":
				destination_group_name = "any"
				## now exit
				break
			elif i['Destination server FQDN'] == "Any":
				destination_group_name = "any"
				## now exit
				break
			elif i['Destination server FQDN'] == "ANY":
				destination_group_name = "any"
				## now exit
				break

			### Create Group for source hosts
			if i['Destination server FQDN']:
				dest_host = i['Destination server FQDN']
				
				destination_group_name = gen_group_name.dst_group(dest_host)
				


	### Do destination hostnames and Destination IP's

	snippet = collection.find({"ruleid" : rule_id})

	print "#### Do Destination addresses #####"
	
	for i in snippet:

		### Check if "any"
		if destination_group_name == "any":
			### EXIT OUT 
			break


		if i['Destination server FQDN'] or i['Dest IP address']:

			
			### ToDo Juniper Code to generate destination hosts

			host = i['Destination server FQDN']
			ip = i['Dest IP address']

			### Generate destination hosts
			host = gen_host(rule_id, host, ip)

			### Todo Juniper Code to generate destination hosts groups / address sets
			add_to_group.add(rule_id, host, destination_group_name)

	
	### Do Services / Applications
	dest_app = []

	snippet = collection.find({"ruleid" : rule_id})

	if not application_set_name:

		for i in snippet:
			### Create Group for source hosts
			if i['Destination server FQDN']:
				dest_host = i['Destination server FQDN']
				source_host = i['Source server FQDN']
				
				application_set_name = gen_group_name.app_set(dest_host, source_host)

	snippet = collection.find({"ruleid" : rule_id})

	print "#### SERVICES / APPLICATIONS SECTION ####"

	

	for i in snippet:
		if i['Service'] or i['Dest Ports'] or i['Protocol']:
	
			###   Juniper Code to generate application services
			service = i['Service']
			dst_port = str(i['Dest Ports'])
			protocol = i['Protocol']

			### Generate applications

			dest_app.append(gen_app.gen_service_app(rule_id, service, dst_port, protocol))

	### Add Apps to Application sets

	for app in dest_app:
		
		add_to_group.app_set(rule_id, app, application_set_name)

	


	### Generate Ruleset based on above juniper configs

	### Generate Policy Name

	snippet = collection.find({"ruleid" : rule_id})

	if not policy_name:

		for i in snippet:
			### Create Policy Name
			if i['Destination server FQDN']:
				dest_host = i['Destination server FQDN']
				source_host = i['Source server FQDN']
				policy_name = gen_group_name.policy_name(dest_host, source_host)

	### Setup Zones

	snippet = collection.find({"ruleid" : rule_id})

	### Source Zone

	if not source_zone:
		for i in snippet:
		### Check for Any - which would then make it a global policy.
		### Check for presence of "Any"
			if i['source zone'] == "any":
				source_zone = "any"
				## now exit
				break
			elif i['source zone'] == "Any":
				source_zone = "any"
				## now exit
				break
			elif i['source zone'] == "ANY":
				source_zone = "any"
				## now exit
				break

			### Create Source Zone Name
			if i['source zone']:
				source_zone = i['source zone']
				
	
	snippet = collection.find({"ruleid" : rule_id})

	### Destination Zone

	if not destination_zone:

		for i in snippet:

			### Check for Any - which would then make it a global policy.
		### Check for presence of "Any" if found then exit loop
			if i['destination zone'] == "any":
				destination_zone = "any"
				## now exit
				break
			elif i['destination zone'] == "Any":
				destination_zone = "any"
				## now exit
				break
			elif i['destination zone'] == "ANY":
				destination_zone = "any"
				## now exit
				break
			### Create Destination Zone Name
			if i['destination zone']:
				destination_zone = i['destination zone']


	### SETUP POLICIES

	print " ####  POLICY SECTION #### "
	policy.gen_policy(rule_id, source_zone, destination_zone, source_group_name, destination_group_name, application_set_name, policy_name)




def gen_host(rule_id, host, ip):

	config1 = "set security address-book global address " 
	config2 = " description "


	#final_config = config1 + host + " " + ip + config2 + "'" + rule_id + "'"
	final_config = config1 + host + " " + ip

	print final_config
	
	### Return config ready to be added to list

	return host

#def add_to_group(rule_id, host)

def get_all_rule_ids(collection):

	all_rule_ids = []

	snippet = collection.find()

	### Only retrieve Unique ID's
	for row in snippet:
		#print row['ruleid']
		try:
			if row['ruleid']:
				all_rule_ids.append(row['ruleid'])
		except:
			pass


	### Make List Unique

	all_rule_ids = list(set(all_rule_ids))

	### Print Unique List of IDs

	#for id in all_rule_ids:
		#print id
		


	return all_rule_ids

def get_all_rules(collection, rule_ids):

	for id in rule_ids:

		### Unique source group name per rule_id so reset it here
		source_group_name = ""
		destination_group_name = ""
		application_set_name = ""
		source_zone = ""
		destination_zone = ""
		policy_name = ""

		get_rule_by_id(collection, id, source_zone, destination_zone, source_group_name, destination_group_name, application_set_name, policy_name)





def main():

	collection = connect_db()

	### Get all rule id's
	all_rule_ids = get_all_rule_ids(collection)

	### Get all rules

	get_all_rules(collection, all_rule_ids)




main()
