#!/bin/sh


if [ "$1" == "already-bin" ]
then
    sudo cp bin/pah /usr/local/bin
fi
if [ "$1" != "already-bin" ]
then
    sudo pacman -Syy python python-pip
    pip install pyinstaller rich 
    python3 -m PyInstaller -F --add-data "libimpl.py:." pah.py
    sudo cp dist/pah /usr/local/bin/
fi

