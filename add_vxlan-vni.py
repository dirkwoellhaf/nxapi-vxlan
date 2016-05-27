#/usr/bin/env oython

import requests
import json
import random

"""
Modify these please
"""
url='http://10.1.18.13/ins'
switchuser='admin'
switchpassword='C15co123!'
cmd_id_start = 2
vland_id_start = 100
vxlan_id_start = vland_id_start + 40000
counter = 1
needed = 3500  #MAX: 3500
nve_interface = 1
mcast_base = "239.0.0.0"

def getMcastAddress(mcast_base,counter,needed):
    mcast = mcast_base.split(".")
    mcast[3] = counter

    #test = needed/255
    #print int((counter/test)/1.5)
    #print random.randint(1,)
    mcast[3] = random.randint(1,512)
    if mcast[3] >= 257:
        mcast[2] = 1
        mcast[3] = int(mcast[3]) - 256

    address = mcast[0]+"."+mcast[1]+"."+str(mcast[2])+"."+str(mcast[3])

    return address


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
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "router bgp 65000", "version": 1 }, "id": 8
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "evpn", "version": 1 }, "id": 9
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "vni "+str(vxlan_id)+" l2", "version": 1 }, "id": 10
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "rd auto", "version": 1 }, "id": 11
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "route-target import auto", "version": 1 }, "id": 12
      },
      {
        "jsonrpc": "2.0", "method": "cli", "params": { "cmd": "route-target export auto", "version": 1 }, "id": 13
      }


    ]

    myheaders={'content-type':'application/json'}
    payload={
      "ins_api": {
        "version": "1.0",
        "type": "cli_conf",
        "chunk": "0",
        "sid": "1",
        "input": "conf t ;vlan "+str(vlan_id)+" ;name PY_"+str(vlan_id)+" ;vn-segment "+str(vxlan_id)+" ;interface nve "+str(nve_interface)+" ;member vni "+str(vxlan_id)+" ;mcast-group "+str(mcast_address)+"" ;router bgp 65000 ;evpn ;vni "+str(vxlan_id)+" l2 ;rd auto ;route-target import auto ;route-target export auto",
        "output_format": "json"
      }
    }

    #print payload
    response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()

# Enable for debugging
    #print response
    #response = ""
    return response

if __name__ == "__main__":
    vland_id = vland_id_start
    vxlan_id = vxlan_id_start

    while counter <= needed:
        response = addSegment(vland_id,vxlan_id,getMcastAddress(mcast_base,counter,needed),nve_interface)

        if "error" in response :
            print "ERROR: "+str(response)


        vland_id = vland_id + 1
        vxlan_id = vxlan_id + 1
        counter = counter + 1
        #print counter

    print "Created " + str(counter-1) + " Segments"
