### main file

import csv
#import yaml
import random
import re


in_file  = open('rest-of-pri.csv', "r")
csv_format_other = True   ### True is name col 1 and ip col 2
is_secondary = False  ### else default to primary

global truncatedName


proxy_list = ["OrangeP02", "OrangeP03", "OrangeP04", "OrangeP05", "OrangeP06", "OrangeP07", "OrangeP08", "OrangeP09", "OrangeP10"]


def truncateName(name):
	
	global truncatedName 
	
	truncatedName = name[:20]

	### get rid of special characters

	truncatedName = re.sub('[^A-Za-z0-9]+', '', truncatedName)

	return truncatedName



def main():

	list_of_zools = get_new_list()

	random_zools = get_random_zools_mapping(list_of_zools)

	config = gen_config(random_zools)

	### Finally print the resulting config

	for c in config:
		print c

def gen_config(random_zools):

	lines = []

	if not is_secondary:
		command1 = "set security nat destination rule-set Pri_Smoothwall8080 rule LB_"
	else:
		command1 = "set security nat destination rule-set Sec_Smoothwall8080 rule LB_"

	config = []

	for zool in random_zools:
		line1 = command1 + zool[0] + " match destination-address 192.168.210.14/32"
		line2 = command1 + zool[0] + " match source-address " + zool[1]
		line3 = command1 + zool[0] + " then destination-nat pool " + zool[2]

		config.append(line1)
		config.append(line2)
		config.append(line3)



	return config

def get_random_zools_mapping(list_of_zools):

	proxy_list_shuffled = random.shuffle(proxy_list)
	#print proxy_list
	random.shuffle(list_of_zools)
	proxy_to_zools = []


	for s in list_of_zools:
		shuffled_proxies = random.sample(proxy_list, len(proxy_list))
		#print s[0] + " " + shuffled_proxies[0]
		mapping = []
		mapping.append(s[0])
		mapping.append(s[1])
		mapping.append(shuffled_proxies[0])

		proxy_to_zools.append(mapping)


	# for item in proxy_to_zools:
	# 	print item

	return proxy_to_zools

	# for x in proxy_list:
	# 	print x





def get_new_list():

	### Parse the CSV and only get the bits we are interested in, put them in a new list of lists and return.

	if not csv_format_other:

		csv_f = csv.reader(in_file)

	 	new_list = []
	 	zool_list =[]

		for row in csv_f:
			new_row = row[0].split(' ')
			new_list.append(new_row)
		
		for i in new_list:
			#print i[1], i[2]
			name = i[1]
			ip = i[2]

			### Create small list for temporary new row
			new_row = []
			new_row.append(name)
			new_row.append(ip)

			### Create new List of lists
			zool_list.append(new_row)
	else:

		### Do other type of CSV file, format:  Name,  IP
		csv_f = csv.reader(in_file)
		new_list = []
	 	zool_list =[]

		for row in csv_f:
			#print row[0]
			#print row[0]
			#print row[1]
			new_row = []
			new_row.append(row[0])
			new_row.append(row[1])   ### IP
			#new_row[0] = row[0]
			#new_row[1] = row[1]
			new_list.append(new_row)
		
		for i in new_list:
			#print i[1], i[2]
			name = truncateName(i[0])
			ip = i[1]

			### Create small list for temporary new row
			new_row = []
			new_row.append(name)

			parsedIp = parseIpSpaces(ip)
			new_row.append(parsedIp)

			### Create new List of lists
			zool_list.append(new_row)



	#print zool_list

	return zool_list

def parseIpSpaces(ip):

	if " " in ip:
		#### put square brackets around the multi IP string
		ip = "[" + ip + "]"

	return ip





main()
