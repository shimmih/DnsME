from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import hmac
import hashlib
import base64
import codecs
import json
import requests
import sys

__author__ = 'Shimmi Harel'

def getKwArgs(arguments):
	'''
	input: sys.argv
	retun: dictionary with all keword arguments (x=y)
	'''
	args = {}
	for i in arguments:
		try:
			k,v = i.split('=')
			args[k] = v
		except Exception as e:
			pass
	return args

args = getKwArgs(sys.argv)
apiKey = args['key']
secretKey = args['secret']
argv1 = args['name']
argv2 = args['target']
argv3 = args['type']
now = datetime.now()
stamp = mktime(now.timetuple())
requestDate = format_date_time(stamp)
domainId = "794461"

url ="https://api.dnsmadeeasy.com/V2.0/dns/managed/"+domainId+"/records/"

data = {"name":argv1,"type":argv3,"value":argv2,"ttl":1800}
data =json.dumps(data)

hexlify = codecs.getencoder('hex')
myHmac = hmac.new(secretKey,requestDate , hashlib.sha1).digest()
hexl =hexlify(myHmac)[0]

headers = { 'x-dnsme-apiKey': apiKey, 'x-dnsme-requestDate':requestDate, 'x-dnsme-hmac':hexl }

print "URL =",url
print "Request Date = ",requestDate
print "name = " + argv1
print "target = " + argv2
print "type = " +argv3
print "data = ", data
print "Headers = " ,headers

try:
    r =  requests.post(url, headers=headers, data=data)
except Exception as e:
    print "Failed to create the record"
    print e
    exit(1)
else:
    exit()


