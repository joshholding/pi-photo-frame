#!/bin/sh

PHOTOS_DIR=/home/pi/Pictures
SLIDESHOW_DELAY=60

#--recursivedir
#--fixed_width
#--fixed_zoom
#--scale_down
#--no_statusbar
#--slide # show slideshow immediately
#--random
#--readyonly
#--shuffle - next/prev buttons
#--delay
#--fullscreen
#--autorotate
#--maxpect  Expand image(s) to fit screen size while preserving aspect ratio.
qiv --watch --maxpect --no_statusbar --slide --random --readonly --fullscreen --autorotate --delay $SLIDESHOW_DELAY --display :0 $PHOTOS_DIR
