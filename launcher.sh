#!/bin/sh
#launcher.sh

cd /
cd home/pi/ceaos-reservoir
sudo python3 setup.py install
cd ceaos_reservoir
sudo python3 driver.py
cd /
