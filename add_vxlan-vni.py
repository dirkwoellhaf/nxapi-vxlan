#/usr/bin/env oython

import requests
import json
import random
import sys


switchuser='admin'
switchpassword='C15co123!'
cmd_id_start = 2
vland_id_start = 100
vxlan_id_start = vland_id_start + 40000
counter = 1
needed = int(sys.argv[1])  #MAX: 3500
nve_interface = 1
mcast_base = "239.0.0.0"

def getMcastAddress(mcast_base):
    mcast = mcast_base.split(".")

    mcast[3] = random.randint(1,512)
    if mcast[3] >= 257:
        mcast[2] = 1
        mcast[3] = int(mcast[3]) - 256

    address = mcast[0]+"."+mcast[1]+"."+str(mcast[2])+"."+str(mcast[3])

    return address


def addSegment (vlan_id,vxlan_id,mcast_address,nve_interface,switches):

    print "Creating VLAN-ID:"+str(vlan_id)+", VXLAN-ID:"+str(vxlan_id)+", MCAST-GROUP:"+str(mcast_address)

    myheaders={'content-type':'application/json'}
    payload={
      "ins_api": {
        "version": "1.0",
        "type": "cli_conf",
        "chunk": "0",
        "sid": "1",
        "input": "vlan "+str(vlan_id)+" ;name PY_"+str(vlan_id)+" ;vn-segment "+str(vxlan_id)+" ;interface nve "+str(nve_interface)+" ;member vni "+str(vxlan_id)+" ;mcast-group "+str(mcast_address)+" ;router bgp 65000 ;evpn ;vni "+str(vxlan_id)+" l2 ;rd auto ;route-target import auto ;route-target export auto",
        "output_format": "json"
      }
    }

    #print payload
    switches = switches.split(",")
    for switch in switches:
        url='http://'+switch+'/ins'
        response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()

# Enable for debugging
    #print response
    #response = ""
    return response

if __name__ == "__main__":
    vland_id = vland_id_start
    vxlan_id = vxlan_id_start


    while counter <= needed:
        response = addSegment(vland_id,vxlan_id,getMcastAddress(mcast_base),nve_interface,sys.argv[2])

        if "Success" not in response :
            print "ERROR: \n"+str(response)


        vland_id = vland_id + 1
        vxlan_id = vxlan_id + 1
        counter = counter + 1
        #print counter

    print "Created " + str(counter-1) + " Segments"
