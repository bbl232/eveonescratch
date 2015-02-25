#!/usr/bin/env/ bash

set -e

#install scratch
sudo apt-get update
sudo apt-get install -y scratch python-pip python-dev build-essential git

git clone https://github.com/bbl232/py-spidev
pushd py-spidev
make
sudo make install
popd

sudo pip install scratchpy

git clone https://github.com/bbl232/eveonescratch
sudo mv eveonescratch /opt/eveonescratch
mkdir -p /home/pi/Desktop
cp /opt/eveonescratch/scratch.desktop $HOME/Desktop/scratch.desktop 

echo "alias scratch='/opt/eveonescratch/start.sh'" >> $HOME/.bashrc
echo "NOTE: You have to run 'sudo raspi-config' and enable SPI in the Advanced options section of the menu."
echo "You will also need to reboot to apply changes."
