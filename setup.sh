#!/bin/sh

pip install rich
chmod +x pah.py
cp pah.py /usr/local/bin/pah
mkdir /usr/lib/pah
cp libimpl.py /usr/local/lib/pah

