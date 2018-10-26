#!/bin/sh
ansibleIPhost=$(openstack server list --name acc3-ansible-op -c Networks -f value | awk '{ split($5, v, "=");split(v[2],x,","); print x[1], "acc3-ansible-op"}')
ansibleIP=$(echo $ansibleIPhost | awk '{split($1, v, " ");print v[1]}')
scp -i /home/ubuntu/acc3-QTLaaS/add-userdata/keys/id_rsa /home/ubuntu/hosts ubuntu@$ansibleIP:/etc/hosts
scp -i /home/ubuntu/acc3-QTLaaS/add-userdata/keys/id_rsa /home/ubuntu/ansible-hosts ubuntu@$ansibleIP:/etc/ansible/hosts
ssh -i /home/ubuntu/acc3-QTLaaS/add-userdata/keys/id_rsa ubuntu@$ansibleIP 'bash -s' < ansible-playbook-command-add.sh
