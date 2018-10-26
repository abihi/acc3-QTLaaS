#!/bin/sh
ansible-playbook -s --private-key /home/ubuntu/.ssh/id_rsa --start-at-task="adding paths" /home/ubuntu/QTLaaS/spark_deployment.yml
