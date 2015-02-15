#!/usr/bin/env bash

cd /opt/eveonescratch
sudo python eve_one_mesh.py &
PID=$!
scratch --document "/opt/eveonescratch/nightlight.sb"
sudo kill $PID
