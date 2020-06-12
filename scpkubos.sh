#!/usr/bin/env bash

ip='192.168.8.2'

# copy over entire directory
sshpass -p "Kubos123" scp -r ~/winsat_kubos/kubos/* kubos@$ip:/home/kubos/

# install main service config file
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/kubos-config.toml kubos@$ip:/etc/

# install service init scripts
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/eps/eps-service/eps-service.init kubos@$ip:/home/system/etc/init.d/S01eps-service   # eps
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/rtc/rtc-service/rtc-service.init kubos@$ip:/home/system/etc/init.d/S01rtc-service   # eps

# install service monit scripts
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/eps/eps-service/eps-service.monit kubos@$ip:/home/system/etc/monit.d/eps-service.cfg   # eps
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/rtc/rtc-service/rtc-service.monit kubos@$ip:/home/system/etc/monit.d/rtc-service.cfg   # eps
