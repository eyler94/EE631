#!/usr/bin/env bash 

sudo apt-get install -y gcc make build-essential python3-dev git scons swig

sudo sh -c 'echo "blacklist snd_bcm2835" >> /etc/modprobe.d/snd-blacklist.conf'

sudo sed -i 's/dtparam=audio=on/#dtparam=audio=on/' /boot/config.txt

git clone https://github.com/jgarff/rpi_ws281x

sleep 3

cd ~/rpi_ws281x

sudo scons 

cd python

sudo python3 setup.py build

sudo python3 setup.py install

#sudo reboot
