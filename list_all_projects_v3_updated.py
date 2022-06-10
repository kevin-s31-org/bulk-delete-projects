from importlib_metadata import NullFinder
import requests
import json
from pprint import pprint
import itertools
import os
import requests
import sys
SNYK_TOKEN=os.getenv('SNYK_TOKEN')



headers= {
 'Content-Type': 'application/vnd.api+json; charset=utf-8',
 'Authorization': 'token '+ SNYK_TOKEN
}

org_id=input(str('enter orgID '))
#print(org_id)

url="https://api.snyk.io/v3"
args="/orgs/{}/projects?version=2021-06-04~beta".format(org_id)
#print(args)
response = requests.request("GET", url+args, headers=headers)
#print(response)
if response.status_code!=200:
   print('OrgID Does Not Exist')
   sys.exit()
else:
   pass

response=response.json()
#pprint(response)

dictionary_is_projects={}
def get_list_of_projects(response):
    for key in response:
        if key =='data':
            new_response=response[key]
            for i in new_response:
                projectID=(i['id'])  #grabs projectID
                name=(i['attributes']['name'])  #grabs name
                project_type=(i['attributes']['type'])
                #print(projectID + ' is project ID',name + ' is name ',project_type+" is project type ")
                if projectID not in dictionary_is_projects:
                    dictionary_is_projects[projectID]=[]
                dictionary_is_projects[projectID].append(project_type)
                
get_list_of_projects(response)
#pprint(dictionary_is_projects)

def loop_next(response):
   while True:
      for key in response:
         if key=='links':
            if 'next' in response[key]:
               links=response[key]['next']
               response=requests.request("GET",url+links,headers=headers)
               response=response.json()
               #pprint(response)
            get_list_of_projects(response)
               #pprint(dictionary_is_projects)
            #elif 'next' not in response[key]:
            #   sys.exit()
            
loop_next(response)
pprint(dictionary_is_projects)