#!/bin/sh

sudo pacman -Syy python python-pip
pip install pyinstaller rich 
python3 -m PyInstaller -F --add-data "libimpl.py:." pah.py
sudo cp dist/pah /usr/local/bin/

