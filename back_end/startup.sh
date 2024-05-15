#!/bin/bash

NOW="$(date +"%Y-%m-%d_%H:%M:%S")"

aws s3 cp s3://unifor-services/dicionario_legislacao.dic ./servico_GCL/

mkdir -p /home/ubuntu/AILA/Logs

sudo chown -R ubuntu:docker /home/ubuntu/AILA/
sudo find /home/ubuntu/AILA/ -type d -exec chmod 775 {} \;
sudo find /home/ubuntu/AILA/ -type f -exec chmod 664 {} \;

cd back_end

sudo docker compose down

sudo docker system prune -f

nohup sudo docker compose up --build > "/home/ubuntu/AILA/Logs/log__$NOW.txt" 2>&1 &