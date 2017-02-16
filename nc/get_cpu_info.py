import ncclient.manager as manager
import xml.dom.minidom
from argparse import ArgumentParser
import xmltodict
import pprint

cpu_util = '''<filter>
<cpu-usage xmlns="urn:cisco:params:xml:ns:yang:cisco-process-cpu">
<cpu-utilization>
</cpu-utilization>
</cpu-usage></filter>'''


cpu_process = '''<filter>
<cpu-usage xmlns="urn:cisco:params:xml:ns:yang:cisco-process-cpu" xmlns:y="http://tail-f.com/ns/rest" xmlns:pcpu="urn:cisco:params:xml:ns:yang:cisco-process-cpu">
<process-cpu-usage>
</process>
</process-cpu-usage>
</filter>'''


if __name__ == '__main__':
  parser = ArgumentParser(description='Select options.')
  # Input parameters
  parser.add_argument('--host', type=str, default='172.20.20.10',
  help="The device IP or DN")
  parser.add_argument('-u', '--username', type=str, default='vagrant')
  parser.add_argument('-p', '--password', type=str, default='vagrant')
  parser.add_argument('--port', type=int, default=830,
  help="Specify this if you want a non-default port")
  args = parser.parse_args()
  m = manager.connect(host=args.host,
                      port=args.port,
                      username=args.username,
                      password=args.password,
                      device_params={'name':"csr"})
  # Pretty print the XML reply
  print ('Using NETCONF, you can present data as XML without any conversion')
  cpu_util = str( m.get( filter=cpu_util ) )
  xmlDom = xml.dom.minidom.parseString(cpu_util)
  print xmlDom.toprettyxml( indent = " " )
  print ('Or you can convert to Dictionary')
  cpu_dict = xmltodict.parse( cpu_util )['rpc-reply']['data']
  print [(i,v) for i,v in cpu_dict['cpu-usage']['cpu-utilization'].iteritems()]
  print ('\nWith structured data you can filter or sort \nHere we are grabbing the processes with higher run-time')
  cpu_dict = xmltodict.parse( str( m.get( filter=cpu_process ) ) )
  cpu_dict = cpu_dict['rpc-reply']['data']
  nonzero_process = [t for t in cpu_dict['cpu-usage']['process-cpu-usage']['process'] if int(t['total-run-time']) > 100]
  pp = pprint.PrettyPrinter(indent=2)
  pp.pprint(nonzero_process)
