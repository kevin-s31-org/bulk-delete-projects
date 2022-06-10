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

#Grab the list of SAST projects and put into dictionary
global projectID_dict
projectID_dict={}
def find_project_ID(response):
   #projectID_dict=[]
   for key in response:
      if key =='data':
         new_response=response[key]
         for key in new_response:
            #pprint(key)
            projectID=(key['id'])  #grabs projectID
            name=(key['attributes']['name'])  #grabs name
            project_type=(key['attributes']['type'])
            if project_type=='sast':
               print(project_type,name)
               if project_type not in projectID_dict:
                  proj={'projectid':projectID}
               else:
                  project={'projectid':None} 
               projectID_dict.update(proj)
               #pprint(projectID_dict)
      else:
         pass


#This loops through all of your orgs for all the project ID's
def loop_next(response):
   while True:
      for key in response:
         if key=='links':
            if 'next' in response[key]:
               links=response[key]['next']
               response=requests.request("GET",url+links,headers=headers)
               response=response.json()
               print(response)
               #find_project_ID(response)
            elif 'next' not in response[key]:
               sys.exit()
            


   else:
      pass

#how to call the function
loop_next(response)



#Get the code issues now
def get_code_issues():
   org_id=input(str('enter orgID '))
   project_ID=input(str('enter projectID '))
   

#get_code_issues()

