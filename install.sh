#! /bin/sh

sudo pip3 install pikepdf
sudo pip3 install rarfile

sudo mkdir /usr/share/filedragon
sudo cp src/main.py /usr/share/filedragon/
chmod +x filedragon
sudo cp filedragon /bin/
