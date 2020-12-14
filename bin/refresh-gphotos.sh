#!/bin/sh
GPHOTOS_LOCAL_DIR=/home/pi/Pictures
GPHOTOS_ALBUM=Favorites

echo "Copying Google Photos Album : $GPHOTOS_ALBUM to: $GPHOTOS_LOCAL_DIR"
rclone copy --progress gphotos:album/$GPHOTOS_ALBUM $GPHOTOS_LOCAL_DIR
pkill qiv
/usr/local/bin/display-photos.sh
