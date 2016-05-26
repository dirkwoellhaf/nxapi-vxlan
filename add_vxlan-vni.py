#/usr/bin/env oython

import requests
import json

"""
Modify these please
"""
url='http://10.1.18.13/ins'
switchuser='admin'
switchpassword='C15co123!'
cmd_id_start = 2
vland_id_start = 101
vxlan_id_start = vland_id_start + 40000
counter = 1
needed = 400

def addVlan (vlan_id,vxlan_id):

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
          "cmd": "vlan "+str(vlan_id),
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "name PY_"+str(vlan_id),
          "version": 1
        },
        "id": 3
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "vn-segment "+str(vxlan_id),
          "version": 1
        },
        "id": 4
      }
    ]
    print payload
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()


if __name__ == "__main__":
    vland_id = vland_id_start
    vxlan_id = vxlan_id_start

    while counter <= needed:
        addVlan(vland_id,vxlan_id)

        vland_id = vland_id + 1
        vxlan_id = vxlan_id + 1
        counter = counter + 1
        #print counter
