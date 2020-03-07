#!/usr/bin/env bash
sudo ip a add 192.168.7.1/16 dev enp9s0
sudo ip link set dev enp9s0 up
ssh kubos@192.168.7.2
