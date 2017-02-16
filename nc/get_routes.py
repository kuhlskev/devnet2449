from argparse import ArgumentParser
import ncclient.manager
import xml.dom.minidom
from ncclient.operations import TimeoutExpiredError
import pprint
  
route_filter = '''
  <routing-state xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
    <routing-instance>
      <ribs>
        <rib>
          <name>ipv4-default</name>
          <address-family xmlns:v4ur="urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing">v4ur:ipv4-unicast</address-family>
          <default-rib>true</default-rib>
          <routes/>
        </rib>
      </ribs>
    </routing-instance>
  </routing-state>
  '''

def main():
  parser = ArgumentParser(description='Select options.')
  # Input parameters
  parser.add_argument('--host', type=str, default='172.20.20.10',
  help="The device IP or DN")
  parser.add_argument('-u', '--username', type=str, default='vagrant')
  parser.add_argument('-p', '--password', type=str, default='vagrant')
  parser.add_argument('--port', type=int, default=830,
  help="Specify this if you want a non-default port")
  args = parser.parse_args()
  nckwargs = dict(
    host=args.host,
    port=args.port,
    hostkey_verify=False,
    username=args.username,
    password=args.password,
    device_params={'name':"csr"}
  )
  m = ncclient.manager.connect(**nckwargs)  
  try:
    print ('Here we are printing the RIB as XML\n')
    c = m.get(filter=('subtree', route_filter))
    xmlDom = xml.dom.minidom.parseString(str(c))
    print (xmlDom.toprettyxml( indent = " " ))
  except TimeoutExpiredError as e:
    print("Operation timeout!")
  except Exception as e:
    print("ERORR severity={}, tag={}".format(e.severity, e.tag))
  
  ns = 'urn:ietf:params:xml:ns:yang:ietf-routing'
  nsmap = dict(rt=ns)
  route_table=[]
  routes = c.data.findall(".//{%s}route" % ns)
  for i, route in enumerate(routes):
    dest = route.xpath('./rt:destination-prefix/text()', namespaces=nsmap)
    hop = route.xpath('./rt:next-hop/rt:next-hop-address/text()', namespaces=nsmap)
    intfc = route.xpath('./rt:next-hop/rt:outgoing-interface/text()', namespaces=nsmap)
    prot = route.xpath('./rt:source-protocol/text()', namespaces=nsmap)
    if len(hop) > 0:
        entry = {'hop':hop[0]}
    if len(intfc) > 0:
        entry = {'intfc':intfc[0]}  
    entry.update({'dest':dest[0], 'prot':prot[0]}) 
    route_table.append(entry)
  raw_input('Hit enter to continue')
  print ('\nOr we can just grab the information that is interesting\n')
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(route_table)  
  m.close_session() 

if __name__ == "__main__":
  main()  