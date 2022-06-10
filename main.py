import json
import requests
import json
from pprint import pprint
import os
from tomlkit import array
SNYK_TOKEN=os.getenv('SNYK_TOKEN')
#import list_all_issues_criticalANDhigh


ProjectIssue={}
projectID='40ff1223-6282-4041-a517-bb18b95a02bd'
issueID='SNYK-DEBIAN8-CURL-573157'


 #print(key, '->', response[key])


"""
for i in response:
   print(i)
   print(type(i))
   response_values=response[i]
   print(type(response_values))
#   print(response_values)
   #print(type(response_values))

"""

#for attr,value in response.__dict__.items():
#   print(attr)

#data_response=json.dumps(response.json())
#pprint(data_response)
#print(type(data_response))
#data_response=json.loads(data_response)
#print(type(data_response))
#for k,i in data_response:
#   print(i)
#for key,v#key)