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

floating_ip = nova.floating_ips.create(nova.floating_ip_pools.list()[0].name)
if floating_ip.ip != None:
    print "floating_ip creation completed."
else:
    print "floating_ip creation failed."

snapshot_ansible = nova.glance.find_image(snapshot_name_ansible)
snapshot_master = nova.glance.find_image(snapshot_name_master)
snapshot_worker = nova.glance.find_image(snapshot_name_worker)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")

cfg_file_path_ansible = os.getcwd()+'/cloud-cfg-ansible-optimized.txt'
cfg_file_path_master = os.getcwd()+'/cloud-cfg-master-optimized.txt'
cfg_file_path_worker = os.getcwd()+'/cloud-cfg-worker-optimized.txt'

if os.path.isfile(cfg_file_path_ansible):
    userdata_ansible = open(cfg_file_path_ansible)
else:
    sys.exit("cloud-cfg-ansible.txt is not in current working directory")
if os.path.isfile(cfg_file_path_master):
    userdata_master = open(cfg_file_path_master)
else:
    sys.exit("cloud-cfg-master.txt is not in current working directory")
if os.path.isfile(cfg_file_path_worker):
    userdata_worker = open(cfg_file_path_worker)
else:
    sys.exit("cloud-cfg-worker.txt is not in current working directory")

secgroups_master = ['default', 'the_securitygroup']
secgroups = ['default']

print "Creating instance master ... "
instance_master = nova.servers.create(name="acc3-master-op", image=snapshot_master, flavor=flavor, userdata=userdata_master, nics=nics,security_groups=secgroups_master)
inst_status_master = instance_master.status
print "Creating instance worker ... "
instance_worker = nova.servers.create(name="acc3-worker1-op", image=snapshot_worker, flavor=flavor, userdata=userdata_worker, nics=nics,security_groups=secgroups)
inst_status_worker = instance_worker.status
print "waiting for 5 seconds.. "
time.sleep(5)

while inst_status_master == 'BUILD' or inst_status_worker == 'BUILD':
    print "Instance: "+instance_master.name+" is in "+inst_status_master+" state"
    print "Instance: "+instance_worker.name+" is in "+inst_status_worker+" state, sleeping for 5 seconds more..."
    time.sleep(5)
    instance_master = nova.servers.get(instance_master.id)
    inst_status_master = instance_master.status
    instance_worker = nova.servers.get(instance_worker.id)
    inst_status_worker = instance_worker.status

print "Instance: "+ instance_master.name +" is in "+ inst_status_master +" state"
if floating_ip.ip != None:
    instance_master.add_floating_ip(floating_ip)
    print "Added floating ip: "+ floating_ip.ip +" to "+ instance_master.name

print "Instance: "+ instance_worker.name +" is in "+ inst_status_worker +" state"

print "Creating instance ansible ... "
instance_ansible = nova.servers.create(name="acc3-ansible-op", image=snapshot_ansible, flavor=flavor, userdata=userdata_ansible, nics=nics,security_groups=secgroups)
inst_status_ansible = instance_ansible.status
print "waiting for 5 seconds.. "
time.sleep(5)

while inst_status_ansible == 'BUILD':
    print "Instance: "+instance_ansible.name+" is in "+inst_status_ansible+" state, sleeping for 5 seconds more..."
    time.sleep(5)
    instance_ansible = nova.servers.get(instance_ansible.id)
    inst_status_ansible = instance_ansible.status

print "Instance: "+ instance_ansible.name +" is in "+ inst_status_ansible +" state"
