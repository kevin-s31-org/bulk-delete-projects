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

values = """
  {
    "filters": {
      "orgs": ["ad0cc2f3-8e9d-44d3-b7fb-8a06733d58b9"],
      "severity": [
        "high",
        "critical"
      ],
      "exploitMaturity": [
        "mature",
        "proof-of-concept",
        "no-known-exploit",
        "no-data"
      ],
      "types": [
        "vuln",
        "license",
        "configuration"
      ],
      "languages": [
        "dockerfile"
      ],
      "projects": [],
      "issues": [],
      "identifier": "",
      "ignored": false,
      "patched": false,
      "fixable": false,
      "isFixed": false,
      "isUpgradable": false,
      "isPatchable": false,
      "isPinnable": false,
      "priorityScore": {
        "min": 0,
        "max": 1000
      }
    }
  }
"""

headers = {
  'Content-Type': 'application/json; charset=utf-8',
  'Authorization': 'token '+ SNYK_TOKEN
}
url="https://snyk.io/api/v1/reporting/issues/latest"
response=requests.post(url,headers=headers, data=values)
#print(response)
#pprint(response.json())
response=response.json()
#pprint(response)

dictionary_of_issues={}
#getting list of issues
def get_list_of_issues(issues):
  for key in response:
    if key =='results':
      issue=response[key]
      #pprint(issue)
      for i in issue:
        projectID=(i['project']['id'])
        projectName=(i['project']['name'])
        issueID=(i['issue']['id'])
        #print("projectID is "+ projectID+ " ProjectName is "+projectName +" "+ "IssueID is " + issueID)
        if projectID not in dictionary_of_issues:
          dictionary_of_issues[projectID]=[]
        dictionary_of_issues[projectID].append(issueID)

get_list_of_issues(response)
pprint(dictionary_of_issues)  #returns dictionary of projectID to vulnID

#retrieving ignores
orgID=input(str('enter orgID '))
projectID=input(str('enter projectID '))
issueID=input(str('enter issueID '))
new_url="https://snyk.io/api/v1/org/%s/project/%s/ignore/%s" %(orgID,projectID,issueID)


new_values="""
{
    "ignorePath": "",
    "reason": "",
    "reasonType": "not-vulnerable",
    "disregardIfFixable": true,
    "expires":"2022-08-29"
}
"""
def retrieve_ignore(orgID,projectID,issueID):
  #print(new_url)
  response=requests.request("GET",new_url,headers=headers)
  if response.status_code!=200:
    print('You have a typo')
    sys.exit()
  else:
    pass
  #print(response.json())
  response=response.json()
  print('This is currently what we see for ignored issues' + str(response))
retrieve_ignore(orgID,projectID,issueID)

def make_ignore(orgID,projectID,issueID):
  #print(new_url)
  response=requests.request("POST",new_url,data=new_values,headers=headers)
  #print(response.status_code)
  if response.status_code!=200:
    print('You have a typo')
    sys.exit()
  else:
    #print(response)
    response=response.json()
    print('you have just added an ignore' + str(response))
make_ignore(orgID,projectID,issueID)