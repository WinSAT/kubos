#!/usr/bin/env bash

ip='192.168.8.2'

# copy over entire directory
scp -r ~/winsat_kubos/kubos/* kubos@$ip:/home/kubos/

# install main service config file
scp ~/winsat_kubos/kubos/kubos-config.toml kubos@$ip:/etc/

# install service init scripts
scp ~/winsat_kubos/kubos/eps/eps-service/eps-service.init kubos@$ip:/home/system/etc/init.d/S01eps-service   # eps

# install service monit scripts
scp ~/winsat_kubos/kubos/eps/eps-service/eps-service.monit kubos@$ip:/home/system/etc/monit.d/eps-service.cfg   # eps