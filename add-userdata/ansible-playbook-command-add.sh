#!/bin/sh
ansible-playbook -s --private-key /home/ubuntu/.ssh/id_rsa --start-at-task="disable IPv6" /home/ubuntu/QTLaaS/spark_deployment.yml
