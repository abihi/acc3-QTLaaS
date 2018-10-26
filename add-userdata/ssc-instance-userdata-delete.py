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

servers = nova.servers.list()

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
        worker_name = "acc3-worker"+str(n-1)+"-op"
        worker_newname_found = True

instance_worker = ""
for server in servers:
    if server.name == worker_name:
       instance_worker = server

print instance_worker
print "Deleting instance worker ... "
nova.servers.delete(instance_worker)
print "waiting for 5 seconds.. "
time.sleep(5)

print "Instance: "+ worker_name +" is deleted."

inputfile = open('/home/ubuntu/hosts', 'r').readlines()
write_file = open('/home/ubuntu/hosts', 'w')
for line in inputfile:
    if worker_name not in line:
        write_file.write(line)
write_file.close()

inputfile = open('/home/ubuntu/ansible-hosts', 'r').readlines()
write_file = open('/home/ubuntu/ansible-hosts', 'w')
for line in inputfile:
    if "sparkworker"+str(n) not in line:
        write_file.write(line)
write_file.close()

subprocess.call("/home/ubuntu/acc3-QTLaaS/add-userdata/ansible-commands.sh")
