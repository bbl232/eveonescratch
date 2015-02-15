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

git clone https://github.com/bbl232/eveonescratch /opt/eveonescratch
cp /opt/eveonescratch/scratch.desktop $HOME/Desktop/scratch.desktop 

sudo modprobe spi_bcm2708
echo spi_bcm2708 | sudo tee -a /etc/modules

echo "alias scratch='/opt/eveonescratch/start.sh'" >> $HOME/.bashrc
sudo echo "sudo python $SCRIPT_DIR/eve_one_mesh.py &" >> /etc/rc.local

sudo cp eve_one_server.sh /etc/init.d/eve_one_server
sudo chmod +x /etc/init.d/eve_one_server

echo "Done installing, reboot? [y/N]"
read r
if [[ "y" == "${r}" ]]; then
    sudo reboot
  else
    echo "You will need to reboot manually to apply changes."
fi
