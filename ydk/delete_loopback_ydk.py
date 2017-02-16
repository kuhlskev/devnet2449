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

# interface to delete
to_del = intf.Interfaces.Interface()

# create a new loopback
to_del.name = 'Loopback666'
res = crud.delete(provider, to_del)

provider.close()

