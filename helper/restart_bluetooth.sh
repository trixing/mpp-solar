#!/bin/bash

svc -d /service/jkbms
pgrep -f /data/mpp-solar/jkbt.py | kill
killall bluepy-helper

/etc/init.d/bluetooth stop
sleep 1
killall hciattach
sleep 1
rmmod hci_uart
sleep 1
modprobe hci_uart
sleep 1
if ! /usr/bin/hciattach -t 10 /dev/ttyS0 bcm43xx 921600 noflow -; then
 /usr/bin/hciattach -t 10 /dev/ttyS0 bcm43xx 921600 noflow -
fi
sleep 1
/etc/init.d/bluetooth start
svc -u /service/jkbms
