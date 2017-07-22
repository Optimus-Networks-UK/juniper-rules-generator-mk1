import yaml
import pprint
import re
from urlparse import urlparse
import time
import socket



yamlFile = '.yaml'



def isgoodipv4(s):
    # pieces = s.split('.')
    # if len(pieces) != 4: return False
    # try: return all(0<=int(p)<256 for p in pieces)
    # except ValueError: return False
    try:
    	socket.inet_aton(s)
    	# valid
      	return True
    except socket.error:
    	# not valid
    	return False

def is_valid_hostname(hostname):
    # if len(hostname) > 255:
    #     return False
    # if hostname[-1] == ".":
    #     hostname = hostname[:-1] # strip exactly one dot from the right, if present
    # allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    # return all(allowed.match(x) for x in hostname.split("."))

    if "any" in hostname:
    	return False
    if "Any" in hostname:
    	return False
    if "ANY" in hostname:
    	return False


    ### Check for domain features

    tld = tldextract.extract(hostname)
    if tld.domain and tld.suffix:
    	return True
    if tld.subdomain and tld.domain and tld.suffix:
    	return True
    
    return False



def parseYaml(yamlFile):

	f = open(yamlFile)
	dataMap = yaml.safe_load(f)
	f.close() 



	return dataMap

#TODO
##Netconf Queries


def check_firewall_ip_exists():

	return False


def check_firewall_policy_exists():

	return False



def newAddress(name, prefix, description, num, currentZone):

	#address = "addr-" + currentZone + "-" + name[:8] + "-" + str(num)
	#address = currentZone + "-" + name[:8] + "-" + str(num)     # with dash
	address = currentZone + "-" + name[:8]  + str(num)		# without dash

	### check if IP or DNS name
	### Check if its an IP first
	#split off the cidr network part
	testPrefix = prefix.split("/")
	#print (testPrefix)
	if isgoodipv4(testPrefix[0]):
		print "set security address-book global address " + address + " " + prefix + " " + "description " + '"' + description + '"'
	### now check if its a DNS
	elif is_valid_hostname(prefix):
		### do it the DNS way if it detects a dns hostname
		print "set security address-book global address " + address + " " + " dns-name " + prefix

	else:
		### standard address that already exists
		#line = "set security address-book global address " + prefix 
		#print line

		return prefix   ## Return an existing prefix / host.
	
	return address


def newAddressSet(name, address, whereTo):


	addressSetName = "grp-" + name[:8] + "-" + whereTo
	print "set security address-book global address-set " + addressSetName + " address " + address

	return addressSetName



def newApplication(name, protocol, destinationPort, description):

	name = name[:8] + "-" + protocol + str(destinationPort)

	print "set applications application " + name + " destination-port " + str(destinationPort) + " protocol " + protocol + " description " + '"' +description + '"'

	return name


def newAppSet(name):


	appSet = "grp-app-" + name[:8]   ### Trimmin name string to 8 characters as long strings prove a problem for NAT

	print "set applications application-set " + appSet + " " + "application " + name

	return appSet


def newPolicy(name, srcZone, dstZone, srcAddr, dstAddr, app, description, permit=True, log=True):

	policyString = "set security policies from-zone " + str(srcZone) + " to-zone " + str(dstZone) + " policy " + name

	print policyString + " match source-address " + srcAddr 			## source address  
	print policyString + " match destination-address " + dstAddr 		## destination address
	print policyString + " match application " + app  					## application
	print policyString + " then permit"									## action
	print policyString + " then log session-init" 						## log
	print policyString + " description " + '"' + str(description) + '"' ## Description




def main():

	dataMap = parseYaml(yamlFile)

	name = dataMap['name']
	srcZone = dataMap['zones']['srcZone']
	dstZone = dataMap['zones']['dstZone']


	### Create Description based on existence of fields in the yaml file.

	if dataMap['changeId'] and dataMap['lanDeskNumber']:
		description = dataMap['description'] + str(dataMap['lanDeskNumber']) + " " + str(dataMap['changeId'])
	elif dataMap['changeId']:
		description = dataMap['description'] + " " + str(dataMap['changeId'])
	elif dataMap['lanDeskNumber']:
		description = dataMap['description'] + " " + str(dataMap['lanDeskNumber'])
	else:
		### Failover to just using a plain old description
		description = dataMap['description']


	## Create src Addresses
	# reset counter
	num = 1
	for zone in dataMap['zones']['srcZone'].iteritems():

		currentZone = str(zone[0]) ### select the zone name

		## iterate through the list in column 1
		## check for any
		for ip in dataMap['zones']['srcZone'][currentZone]:
			if ip == "any" or ip == "Any" or ip == "ANY":
				srcAddrSet = ip
				break
			addrName = newAddress(name, ip, description, num, currentZone)
			num += 1
			srcAddrSet = newAddressSet(name, addrName, "src")


	## Create dst Addresses
	## reset ip

	for zone in dataMap['zones']['dstZone']:
	
		currentZone = zone ### select the zone name

		## now iterate through the selected key using the currentZone as the key!
		for ip in dataMap['zones']['dstZone'][currentZone]:
			#print(ip)
			if ip == "any" or ip == "Any" or ip == "ANY":
				dstAddrSet = ip
				break
			addrName = newAddress(name, ip, description, num, currentZone)
			dstAddrSet = newAddressSet(name, addrName, "dst")
			num += 1

	## Create tcp apps
	## Check exists as might return None type.
	if dataMap['app']['dstPortTcp']:
		for appTcp in dataMap['app']['dstPortTcp']:
			#print appTcp
			appName = newApplication(name, "tcp", appTcp, description)
			appSet = newAppSet(appName)

	## Check exists as might return None type.
	if dataMap['app']['dstPortUdp']:
		## Create udp apps
		for appUdp in dataMap['app']['dstPortUdp']:
			#print appUdp
			appName = newApplication(name, "udp", appUdp, description)
			appSet = newAppSet(appName)

	## Create policy
    #def newPolicy(name, srcZone, dstZone, srcAddr, dstAddr, app, permit=True, log=True)
    # create policy per zone context (based on number of source zones and single destination zone)
	for context in dataMap['zones']['srcZone'].iteritems():
		#print(context)
		srcZone = context[0]
		#print "Source Zone : " + str(srcZone)
		dstZone = ""

		for dstZones in dataMap['zones']['dstZone'].iteritems():
			dstZone = dstZones[0]
			#print dstZone



			newPolicy(name, srcZone, dstZone, srcAddrSet, dstAddrSet, appSet, description)
	


### Entry point run
main()





