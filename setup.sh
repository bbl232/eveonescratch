#!/usr/bin/env/ bash

set -e

SCRIPT_DIR=`pwd`

#install scratch
sudo apt-get update
sudo apt-get install -y scratch python-pip python-dev build-essential git

git clone https://github.com/bbl232/py-spidev
pushd py-spidev
make
sudo make install
popd

sudo pip install stratchpy

git clone https://github.com/bbl232/eveonescratch
sudo mv eveonescratch /opt/eveonescratch
cp /opt/eveonescratch/scratch.desktop $HOME/Desktop/scratch.desktop 

sudo modprobe spi_bcm2708
echo spi_bcm2708 | sudo tee -a /etc/modules

echo "alias scratch='/opt/eveonescratch/start.sh'" >> $HOME/.bashrc
echo "You will need to reboot manually to apply changes."
