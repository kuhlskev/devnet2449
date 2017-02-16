#!/usr/bin/env python

from ncclient import manager
import sys
import xml.dom.minidom
from subprocess import Popen, PIPE, STDOUT

# the variables below assume the user is leveraging the
# network programmability lab and accessing csr1000v
# use the IP address or hostname of your CSR1000V device
HOST = '172.20.20.10'
# use the NETCONF port for your CSR1000V device
PORT = 830
# use the user credentials for your CSR1000V device
USER = 'vagrant'
PASS = 'vagrant'
SCHEMA_TO_GET = 'ietf-interfaces'


def main():
    """
    Main method that prints netconf capabilities of remote device.
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         look_for_keys=False, allow_agent=False) as m:
        # print YANG module
        print(' We are connecting to the device and downloading the YANG Module')
        print('***Saving %s YANG Module locally***\n' %SCHEMA_TO_GET)
        data = m.get_schema(SCHEMA_TO_GET)
        xml_doc = xml.dom.minidom.parseString(data.xml)
        yang_module = xml_doc.getElementsByTagName("data")

        # save the YANG module to a file
        with open(SCHEMA_TO_GET+'.yang', mode='w+') as f:
            f.write(yang_module[0].firstChild.nodeValue)
        print("Now we will do a 'pyang -f tree of %s.yang'" % SCHEMA_TO_GET)
        print('This structure is what data we can get (ro/rw) or set (rw)')
        c = m.get_schema(SCHEMA_TO_GET)
    p = Popen(['pyang', '-f', 'tree'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(input=c.data)[0]
    print stdout_data

if __name__ == '__main__':
    sys.exit(main())
