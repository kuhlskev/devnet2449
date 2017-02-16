from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.ietf import ietf_interfaces as intf
from ydk.models.ietf import iana_if_type as iftype

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

# new interface
new_loopback = intf.Interfaces.Interface()

# create a new loopback
new_loopback.name = 'Loopback666'
new_loopback.type = iftype.SoftwareloopbackIdentity()
new_loopback.description = 'Created by Einar'
res = crud.create(provider, new_loopback)

provider.close()

