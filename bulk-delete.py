from importlib_metadata import NullFinder
import requests
import json
from pprint import pprint
import itertools
import os
import requests
import sys
from string import Template
SNYK_TOKEN=os.getenv('SNYK_TOKEN')

""" Valid Type:
        "node",
        "javascript",
        "ruby",
        "java",
        "scala",
        "python",
        "golang",
        "php",
        "dotnet",
        "swift-objective-c",
        "elixir",
        "docker",
        "linux",
        "dockerfile",
        "terraform",
        "kubernetes",
        "helm",
        "cloudformation"
        "sast"
"""



values = """
  {
    "filters": {
      "name": "",
      "origin": "azure-repos",
      "type": ""
    }
  }
"""
org_id=input(str('enter orgID '))
headers = {
  'Content-Type': 'application/json; charset=utf-8',
  'Authorization': 'token '+ SNYK_TOKEN
}
url="https://snyk.io/api/v1/org/%s/projects" %(org_id)
#print(url)
response=requests.post(url,headers=headers, data=values)
#pprint(response.json())
if response.status_code!=200:
   print('OrgID Does Not Exist')
   sys.exit()
else:
   pass
response=response.json()
#pprint(response)

dictionary_of_projects={}
def get_list_of_projects():
    for key in response:
        #pprint(response[key])
        if key=='projects':
            for i in response[key]:
                project_id=i['id']
                project_name=i['name']
                #print(project_id,project_name)
                if project_id not in dictionary_of_projects:
                    dictionary_of_projects[project_id]=[]
                dictionary_of_projects[project_id].append(project_name)

get_list_of_projects()

#pprint(dictionary_of_projects) #dictionary of projects from v1 endpoint add v3 later\
page={}
new_url="https://snyk.io/api/v1/org/"+str(org_id)+"/project/%s"
def assign_projectid_to_url():
    for i in dictionary_of_projects:
        #print(i)
        if i not in page:
            page[i]=[]
            page[i].append(new_url %i)
        #page=(new_url %i)
    #pprint(page)
assign_projectid_to_url()
#print(page)

#project_id=0
#new_url="https://snyk.io/api/v1/org/%s/project/%s" %(org_id,project_id)
def delete_project():
    for i in page:
        string_url=("".join((page[i])))
        #print(string_url)
        newresponse=requests.request("DELETE",string_url,headers=headers)
        print('deleting ' + "".join((dictionary_of_projects[i])))
        #print(newresponse)
    if newresponse.status_code!=200:
        print(newresponse.status_code)
        print('Try again')
        sys.exit()
    else:
        print('All Relevant Projects Deleted')
#delete_project()



def delete_targets():
    v3url="https://api.snyk.io/v3"
    args="/orgs/"+str(org_id)+'/targets?version=2022-04-06~beta'
    print(v3url+args)
    response = requests.request("GET", v3url+args, headers=headers)
    #print(response)
    if response.status_code!=200:
        print('OrgID Does Not Exist')
        sys.exit()
    else:
        pass
    response=response.json()
    for i in response:
        pprint(response[i])
delete_targets()

"""
def loop_next():
   while True:
      for key in response:
         if key=='links':
            if 'next' in response[key]:
               links=response[key]['next']
               response=requests.request("GET",url+links,headers=headers)
               response=response.json()
               pprint(response)
            delete_targets()
               #pprint(dictionary_is_projects)
            #elif 'next' not in response[key]:
            #   sys.exit()
            
loop_next()
"""