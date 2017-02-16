from argparse import ArgumentParser
import jtextfsm as textfsm
from netmiko import ConnectHandler
import pprint

def get_show_ip_route(ip, username, password, enable_secret):
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
    result += ssh_connection.send_command("show ip route", delay_factor=2)
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
    raw_text_data = get_show_ip_route(host, username, password, enable_secret)
    print ('This is what the text looks like\n' + raw_text_data)
  except Exception as ex:
    print("Exception occurred: %s" % ex)