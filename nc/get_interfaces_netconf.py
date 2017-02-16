#!/usr/bin/env python
from ncclient import manager
import sys
import xml.dom.minidom


# the variables below assume the user is leveraging the
# network programmability lab and accessing csr1000v
# use the IP address or hostname of your CSR1000V device
HOST = '172.20.20.10'
# use the NETCONF port for your CSR1000V device
PORT = 830
# use the user credentials for your CSR1000V device
USER = 'vagrant'
PASS = 'vagrant'
# XML filter
CONF_FILTER ='''<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces>
</filter>'''
STATE_FILTER ='''<filter>
  <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
  </interfaces-state>
</filter>'''


# create a main() method
def main():
    """
    Main method that retrieves the interfaces from config via NETCONF.
    """
    with manager.connect(host=HOST, port=PORT, username=USER,
                         password=PASS, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        """
        Simple main method calling our function.
        """
        print('\nHere is the XML data for Interfaces Operational State')
        interfaces = m.get(STATE_FILTER)
        print(xml.dom.minidom.parseString(interfaces.xml).toprettyxml())
        raw_input("Enter to Continue")
        print('\nHere is the XML data for Interfaces Configuration')
        interfaces = m.get_config('running',CONF_FILTER)
        print(xml.dom.minidom.parseString(interfaces.xml).toprettyxml())

if __name__ == '__main__':
    sys.exit(main())
