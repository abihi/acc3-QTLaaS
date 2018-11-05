#!/bin/sh
ansible-playbook -s --private-key /home/ubuntu/.ssh/id_rsa --start-at-task="start spark worker process" /home/ubuntu/QTLaaS/spark_deployment.yml
