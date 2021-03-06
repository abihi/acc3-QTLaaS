# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, subprocess
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

servers = nova.servers.list()

ansible_found = False
master_found = False
worker_found = False

for server in servers:
  if server.name == "acc3-ansible-op":
        ansible_found = True
  if server.name == "acc3-master-op":
        master_found = True
  if server.name == "acc3-worker1-op":
        worker_found = True

#Check if initial setup exists
if ansible_found != True:
    sys.exit("Error: ansible node not active!")
if master_found != True:
    sys.exit("Error: master node not active!")
if worker_found != True:
    sys.exit("Error: worker node not active!")

snapshot_worker = nova.glance.find_image(snapshot_name_worker)
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

n = 1
worker_name = "acc3-worker"+str(n)+"-op"
worker_newname_found = False
while worker_newname_found != True:
    local_found = False
    for server in servers:
        if server.name == worker_name:
           local_found = True
    if local_found:
        n = n + 1
        worker_name = "acc3-worker"+str(n)+"-op"
    else:
        worker_newname_found = True

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

instance_worker_ip = str(instance_worker.networks['SNIC 2018/10-30 Internal IPv4 Network'][0])

print "Instance: "+instance_worker.name+" is in "+inst_status_worker+" state"
print instance_worker_ip
time.sleep(10)

with open('/home/ubuntu/hosts', "a") as hosts_file:
    hosts_file.write("\n")
    hosts_file.write(instance_worker_ip + " " + instance_worker.name + "\n")

with open('/home/ubuntu/ansible-hosts', "a") as ansible_file:
    ansible_file.write("\n")
    ansible_file.write("sparkworker"+ str(n) + " ansible_connection=ssh ansible_user=ubuntu" + "\n")

configString = "[configNode]"
inputfile = open('/home/ubuntu/ansible-hosts', 'r').readlines()
write_file = open('/home/ubuntu/ansible-hosts', 'w')
for line in inputfile:
    if configString in line:
        new_line = "sparkworker"+ str(n) + " ansible_ssh_host=" + instance_worker_ip
        write_file.write(new_line + "\n")
    write_file.write(line)

write_file.close()

subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/ansible-commands-add.sh")
