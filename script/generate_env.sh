#!/usr/bin/env bash

echo "Input DB username: "
read dbadminusername
echo "Input DB pass: "
read dbadminpass
echo "Input DB website username: "
read dbwbusername
echo "Input DB website pass: "
read dbwbpass

cd /etc/profile.d/
sudo touch bot_env.sh
sudo chmod -R 777 ./bot_env.sh

echo -e "\
export MONGO_DB_ROOT_USERNAME=${dbadminusername}
export MONGO_DB_ROOT_PASSWORD=${dbadminpass}
export MONGO_DB_ROOT_URL=mongodb://${dbadminusername}:${dbadminpass}@mongo:27017/?authSource=admin
export MONGO_DB_ROOT_AUTH_USERNAME=${dbwbusername}
export MONGO_DB_ROOT_AUTH_PASSWORD=${dbwbpass}
" >> bot_env.sh