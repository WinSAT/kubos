#!/usr/bin/env bash
sudo ip a add 192.168.7.1/16 dev $0
sudo ip link set dev $0 up
ssh kubos@192.168.7.2
