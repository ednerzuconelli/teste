#!/bin/bash
git fetch origin
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
if [ $LOCAL != $REMOTE ]; then
   git pull origin main
   sudo systemctl restart server.service
   echo "Projeto atualizado e serviço reiniciado em $(date)" > /home/kuro/update_log.txt
fi