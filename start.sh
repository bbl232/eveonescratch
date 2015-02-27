#!/usr/bin/env bash

sudo modprobe i2c-dev
sudo modprobe i2c-bcm2708

cd /opt/eveonescratch
sudo python eve_one_mesh.py &
PID=$!
scratch --document "/opt/eveonescratch/nightlight.sb"
sudo kill $PID
