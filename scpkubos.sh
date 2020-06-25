#!/usr/bin/env bash

ip='192.168.8.2'

# copy over entire directory
sshpass -p "Kubos123" scp -r ~/winsat_kubos/kubos/* kubos@$ip:/home/kubos/

# install main service config file
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/kubos-config.toml kubos@$ip:/etc/

# install service init scripts
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/eps/eps-service/eps-service.init kubos@$ip:/home/system/etc/init.d/S01eps-service                    # eps
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/rtc/rtc-service/rtc-service.init kubos@$ip:/home/system/etc/init.d/S01rtc-service                    # rtc
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/payload/payload-service/payload-service.init kubos@$ip:/home/system/etc/init.d/S01payload-service    # payload
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/adcs/adcs-service/adcs-service.init kubos@$ip:/home/system/etc/init.d/S01adcs-service                # adcs
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/radio/radio-service/radio-service.init kubos@$ip:/home/system/etc/init.d/S01radio-service            # radio

# install service monit scripts
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/eps/eps-service/eps-service.monit kubos@$ip:/home/system/etc/monit.d/eps-service.cfg                 # eps
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/rtc/rtc-service/rtc-service.monit kubos@$ip:/home/system/etc/monit.d/rtc-service.cfg                 # rtc
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/payload/payload-service/payload-service.monit kubos@$ip:/home/system/etc/monit.d/payload-service.cfg # payload
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/adcs/adcs-service/adcs-service.monit kubos@$ip:/home/system/etc/monit.d/adcs-service.cfg             # adcs
sshpass -p "Kubos123" scp ~/winsat_kubos/kubos/radio/radio-service/radio-service.monit kubos@$ip:/home/system/etc/monit.d/radio-service.cfg         # radio
