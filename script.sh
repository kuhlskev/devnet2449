#!/bin/bash
# Prepare environment for DEVNET2449 Lab
case "$1" in

1) echo "python cli/show_inventory_to_dict.py"
   python cli/show_inventory_to_dict.py
   ;;
#look at textfsm for show inventory
#python cli/show_inventory_to_dict.py --host 'ad3-3850-1' -u 'kekuhls' -p 'kekuhls'
# will need a different device as vpn likley will break vm comms

2) echo "python cli/show_routes.py"
    python cli/show_routes.py
   ;;
#hard to write fsm for

3) echo "python nc/get_routes.py"
   python nc/get_routes.py
   ;;

4) echo "python nc/get_cpu_info.py"
   python nc/get_cpu_info.py
   ;;

5) echo "python nc/get_interfaces_netconf.py"
   python nc/get_interfaces_netconf.py
   ;;
# look at xml and structure of nc calls

6) echo "python get_ietf_interfaces_schema.py"
   python get_ietf_interfaces_schema.py
   ;;
# look at the YANG

7) echo "python ydk/get_interfaces_ydk.py"
   python ydk/get_interfaces_ydk.py
   ;;

#look over code, simpler, more pythonic, proggrammer interface to network devices
8) echo "python ydk/create_loopback_ydk.py"
   python ydk/create_loopback_ydk.py
   ;;

9) echo "python ydk/delete_loopback_ydk.py"
   python ydk/delete_loopback_ydk.py
   ;;

esac