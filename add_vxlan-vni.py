#/usr/bin/env oython

import requests
import json

"""
Modify these please
"""
url='http://10.1.18.13/ins'
switchuser='admin'
switchpassword='C15co123!'

myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "conf t",
      "version": 1
    },
    "id": 1
  },
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "vlan 100",
      "version": 1
    },
    "id": 2
  }
]
print payload
#response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
