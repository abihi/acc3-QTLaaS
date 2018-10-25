#!/bin/sh
ansibleIPhost=$(openstack server list --name acc3-ansible-op -c Networks -f value | awk '{ split($5, v, "=");split(v[2],x,","); print x[1], "acc3-ansible-op"}')
scp -i /home/ubuntu/optimized-test/add-userdata/keys/id_rsa /home/ubuntu/hosts ubuntu@$ansibleIPhost:/etc/hosts
scp -i /home/ubuntu/optimized-test/add-userdata/keys/id_rsa /home/ubuntu/ansible-hosts ubuntu@$ansibleIPhost:/etc/ansible/hosts
