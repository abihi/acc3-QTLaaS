#!/bin/sh
echo StrictHostKeyChecking no | sudo tee -a /etc/ssh/ssh_config
sudo chmod 600 /home/ubuntu/acc3-QTLaaS/add-userdata/keys/id_rsa
