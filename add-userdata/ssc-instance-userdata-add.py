# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ACCHT18.normal"
private_net = "SNIC 2018/10-30 Internal IPv4 Network"
floating_ip_pool_name = "Public External IPv4 network"
floating_ip = None
image_name = "Ubuntu 16.04 LTS (Xenial Xerus) - latest"
snapshot_name_ansible = "IMPORTANT-acc3-ansible-full"
snapshot_name_master  = "IMPORTANT-acc3-master-full"
snapshot_name_worker  = "IMPORTANT-acc3-worker-full"

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print "user authorization completed."

#Check if initial setup exists
instance_ansible = nova.servers.get("acc3-ansible-op")
instance_master = nova.servers.get("acc3-master-op")
instance_worker = nova.servers.get("acc3-worker-op")

if instance_ansible.status != 'ACTIVE':
    sys.exit("Error: ansible node not active!")
if instance_master.status != 'ACTIVE':
    sys.exit("Error: master node not active!")
if instance_worker.status != 'ACTIVE':
    sys.exit("Error: worker node not active!")

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

cfg_file_path_worker = os.getcwd()+'/cloud-cfg-worker-optimized.txt'

if os.path.isfile(cfg_file_path_worker):
    userdata_worker = open(cfg_file_path_worker)
else:
    sys.exit("cloud-cfg-worker.txt is not in current working directory")

secgroups = ['default']

n = 2
worker_name = "acc3-worker"+n+"-op"

print "Creating instance worker ... "
instance_worker = nova.servers.create(name=worker_name, image=snapshot_worker, flavor=flavor, userdata=userdata_worker, nics=nics,security_groups=secgroups)
inst_status_worker = instance_worker.status
print "waiting for 5 seconds.. "
time.sleep(5)

while inst_status_worker == 'BUILD':
    print "Instance: "+instance_worker.name+" is in "+inst_status_worker+" state, sleeping for 5 seconds more..."
    time.sleep(5)
    instance_worker = nova.servers.get(instance_worker.id)
    inst_status_worker = instance_worker.status

print "Instance: "+ instance_worker.name +" is in "+ inst_status_worker +" state"