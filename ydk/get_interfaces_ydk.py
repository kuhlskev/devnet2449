#!/usr/bin/env python
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.ietf import ietf_interfaces as intf

HOST = '172.20.20.10'
PORT = 830
USER = 'vagrant'
PASS = 'vagrant'

# create NETCONF provider
provider = NetconfServiceProvider(address=HOST,
                                  port=PORT,
                                  username=USER,
                                  password=PASS)

# create CRUD service
crud = CRUDService()

# query object
q_i = intf.Interfaces()

# get stuff
intfs = crud.read(provider, q_i)

# print interface names and types
for i in intfs.interface:
    print('%s, %s, %s' % (i.name, i.type._meta_info().yang_name, i.description))
# Or just the tuple with name and enabled to see what ints are up
print [(i.name, i.enabled) for i in intfs.interface]

# query object
q_i = intf.InterfacesState()

# get stuff
intfs = crud.read(provider, q_i)

int_info=[(i.name, i.statistics.out_pkts, int(i.speed)/1000000, i.oper_status) for i in intfs.interface]
for thing in int_info: print(str(thing))

# close the provider
provider.close()


#>>> dir (intfsstate.interface[0])
#['AdminStatusEnum', 'Bandwidth', 'OperStatusEnum', 'Statistics', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_common_path', '_has_data', '_meta_info', '_prefix', '_revision', 'admin_status', 'bandwidth', 'higher_layer_if', 'i_meta', 'if_index', 'is_config', 'last_change', 'lower_layer_if', 'name', 'oper_status', 'parent', 'phys_address', 'speed', 'statistics', 'type']
#>>> dir (intfs.interface[0])
#['LinkUpDownTrapEnableEnum', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_common_path', '_has_data', '_meta_info', '_prefix', '_revision', 'description', 'enabled', 'i_meta', 'is_config', 'link_up_down_trap_enable', 'name', 'parent', 'type']
#>>> dir( intfsstate.interface[0].statistics)
#['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_common_path', '_has_data', '_meta_info', '_prefix', '_revision', 'discontinuity_time', 'i_meta', 'in_broadcast_pkts', 'in_discards', 'in_errors', 'in_multicast_pkts', 'in_octets', 'in_pkts', 'in_unicast_pkts', 'in_unknown_protos', 'is_config', 'out_broadcast_pkts', 'out_discards', 'out_errors', 'out_multicast_pkts', 'out_octets', 'out_pkts', 'out_unicast_pkts', 'parent']
