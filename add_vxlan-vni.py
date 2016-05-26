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
needed = 600
nve_interface = 1
mcast_base = "239.0.0.0"

def getMcastAddress(mcast_base,counter):
    mcast = mcast_base.split(".")
    mcast[3] = counter

    test = counter/256
    if round(test,0) >= 1:
        mcast[2] = int(mcast[2]) + int(round(test,0))
        mcast[3] = int(mcast[3]) - (int(round(test,0)*255))

    return mcast[0]+"."+mcast[1]+"."+str(mcast[2])+"."+str(mcast[3])


def addSegment (vlan_id,vxlan_id,mcast_address,nve_interface):

    print "Creating VLAN-ID:"+str(vlan_id)+", VXLAN-ID:"+str(vxlan_id)+", MCAST-GROUP:"+str(mcast_address)

    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "conf t","version": 1 }, "id": 1
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "vlan "+str(vlan_id), "version": 1 }, "id": 2
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "name PY_"+str(vlan_id), "version": 1 }, "id": 3
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "vn-segment "+str(vxlan_id), "version": 1 }, "id": 4
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "interface nve "+str(nve_interface), "version": 1 }, "id": 5
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "member vni "+str(vxlan_id), "version": 1 }, "id": 6
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "mcast-group "+str(mcast_address), "version": 1 }, "id": 7
      }
    ]
    #print payload
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()


if __name__ == "__main__":
    vland_id = vland_id_start
    vxlan_id = vxlan_id_start

    while counter <= needed:

        addSegment(vland_id,vxlan_id,getMcastAddress(mcast_base,counter),nve_interface)

        vland_id = vland_id + 1
        vxlan_id = vxlan_id + 1
        counter = counter + 1
        #print counter
        
    print "Created " + str(counter) + "Segments"
