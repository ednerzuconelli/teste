#!/bin/bash
PROJECT_DIR="/home/kuro/change"
cd $PROJECT_DIR
git fetch origin
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
if [$LOCAL != $REMOTE]; then
  git pull origin main
  sudo systemctl restart server.service
  echo "Projeto atualizado e serviço reiniciado em $(date)" >> /var/log/update_log.txt
else
  echo "Nenhuma atualização encontrada em $(date) "  >> /var/log/update_log.txt
fi