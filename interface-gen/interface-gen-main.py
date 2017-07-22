import pymongo




def main():

	start()


	
def start():

	collection = connect_db()

	all_interfaces_dataset = collection.find()


	#for i in all_interfaces_dataset:
#		if i['reth_no']:#
			#print i

	gen_interfaces(all_interfaces_dataset)


def connect_db():



	client = pymongo.MongoClient("mongodb://admin:Thespiandelights862@10.55.88.211/admin")
	db = client['import-1']

	collection = db['interface-list']

	return collection

def gen_interfaces(all_interfaces_dataset):

	for interface in all_interfaces_dataset:
		if interface['reth_no']:
			gen_interface(interface)
			gen_routing(interface)
			gen_zones(interface)



def gen_interface(interface):

	print "####### FIREWALL ####### " + interface['fw']
	print "set interfaces " + interface['reth_no'] +"." +str(interface['vlan']) + " family inet address " + interface['iface_ip']
	print "set interfaces " + interface['reth_no'] +"." +str(interface['vlan']) + " vlan-id " + str(interface['vlan'])
	print "set interfaces " + interface['reth_no'] +"." +str(interface['vlan']) + " description " + '"'+interface['comment']+'"'

def gen_routing(interface):

	print "set routing-instances " + interface['routing_instance'] + " interface " + interface['reth_no'] +"." +str(interface['vlan'])


def gen_zones(interface):

	print "set security zones security-zone " + interface['zone'] + " interfaces " + interface['reth_no'] +"." +str(interface['vlan'])
	print "set security zones security-zone " + interface['zone'] + " host-inbound-traffic system-services ping"  
	print "set security zones security-zone " + interface['zone'] + " host-inbound-traffic system-services traceroute" 

main()
