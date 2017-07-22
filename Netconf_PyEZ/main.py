from pprint import pprint
from jnpr.junos import Device
#from jnpr.junos.op.policy import policyTable
from jnpr.junos.op.policy import matchTable
from jnpr.junos.op.arp import ArpTable
from lxml import etree
from jnpr.junos.factory import loadyaml
from jnpr.junos.factory.factory_loader import FactoryLoader

import yaml




srx = Device(host='10.32.2.150', user='automate', password='4LLtheThing5')
srx.open()

#data = policyTable(srx)
data = matchTable(srx)
data.get()

#data.savexml('exported-xml.xml')

print data

#for i in data:
#	print i.name

# for d in data:
# 	print v.data




### Test code

# data = srx220.rpc.get_firewall_policies()
# print data
# print "**** PRINTING XPATH ****"
# print data.xpath("security-context/policies/policy-information")



# pts = policyTable(path='srx.xml')
# pts.get()
# for pt in pts:
#     print 'pt.name: ', pt.name
#     print 'pt.state: ', pt.state
#     print 'pt.seq_no: ', pt.seq_no




