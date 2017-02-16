from argparse import ArgumentParser
import jtextfsm as textfsm
from netmiko import ConnectHandler
import pprint

# see http://jedelman.com/home/programmatic-access-to-cli-devices-with-textfsm/
# for a nice writeup on using textfsm to structure unstructured data
# Try against a real device for more interesting output, for example:
# python cli/show_inventory_to_dict.py --host 'ad3-3850-1' -u 'kekuhls' -p 'kekuhls'

def get_show_inventory(ip, username, password, enable_secret):
    """
    get the inventory from the device using SSH

    :param ip: IP address of the device
    :param username: username used for the authentication
    :param password: password used for the authentication
    :param enable_secret: enable secret
    :return:
    """
    # establish a connection to the device
    ssh_connection = ConnectHandler(
        device_type='cisco_ios',
        ip=ip,
        username=username,
        password=password,
        secret=enable_secret)
    # enter enable mode
    ssh_connection.enable()
    # prepend the command prompt to the result (used to identify the local device)
    result = ssh_connection.find_prompt() + "\n"
    # execute the show inventory command with extended delay
    result += ssh_connection.send_command("show inventory", delay_factor=2)
    # close SSH connection
    ssh_connection.disconnect()
    return result

if __name__ == "__main__":
  parser = ArgumentParser(description='Select options.')
  # Input parameters
  parser.add_argument('--host', type=str, default='172.20.20.10',
    help="The device IP or DN")
  parser.add_argument('-u', '--username', type=str, default='vagrant')
  parser.add_argument('-p', '--password', type=str, default='vagrant')
  parser.add_argument('-e', '--enable', type=str, default='cisco',
    help="Specify this if you want a non-default port")
  parser.add_argument('-s', '--search', type=str, default='SFP-10G-SR', 
  	help='Search for product id in device or devices i.e. SFP-10G-SR')
  parser.add_argument('-f', '--seed_file', type=str, default='None',
  	help='Seed file of devices to ingest')
  args = parser.parse_args()
  host=args.host
  username=args.username
  password=args.password
  enable_secret=args.enable
  sought_product =args.search

  try:
    raw_text_data = get_show_inventory(host, username, password, enable_secret)
    print ('This is what the text looks like\n' + raw_text_data)
    # Run the text through the FSM. 
    # The argument 'template' is a file handle and 'raw_text_data' is a 
    # string with the content from the show_inventory.txt file
    try:
      template = open("show_inventory_multiple.textfsm")
    except:
      template = open("/home/docker/cli/show_inventory_multiple.textfsm")
    re_table = textfsm.TextFSM(template)
    fsm_results = re_table.ParseText(raw_text_data)
    # build keys for inventory sub-items 
    keys = [s for s in re_table.header]
    #build inventory list of dictionaries
    inventory = []
    for row in fsm_results:
      entry = {}
      for i, item in enumerate(row):
        entry.update({keys[i]:item})
      inventory.append(entry)
    pp = pprint.PrettyPrinter(indent=2)
    raw_input("")
    print('Results translated through regular expression template organized as a dictonary')
    pp.pprint(inventory) # Print full inventory as dictionary
    #print([key for key, value in inventory[0].items()])  # print key values as list
    #for item in inventory:   # print inventory elements a table 
    #  print([item[key] for key in item])
    resultlist = [d for d in inventory if d.get('productid', '') == sought_product]
    raw_input("")
    print('\nFound Devices with specific productid ' + sought_product)
    pp.pprint(resultlist) #print list of devices with sought productid
    #print ([(item['hostname'], item['productid']) for item in resultlist])  #print found items as a tuple
  except Exception as ex:
    print("Exception occurred: %s" % ex)