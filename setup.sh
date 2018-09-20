#!/bin/bash

DIR=`pwd`

cp desktop/g.desktop ~/Desktop/guess.desktop
sudo ln -s $DIR/main.py /usr/sbin/guess-that-song
