# pi-picture-frame

Some customizations to a raspberry pi 3 turned into a picture frame. These are just some notes for myself or anyone else.

## Docs/Setup Notes
* **bin/MotionDetectDisplayControl.py** manages PIR and turning on/off the monitor via HDMI
  * add as service to */lib/systemd/system/motiondetect.service*:
    '[Unit]
     Description=Motion Detect Display Control
     After=multi-user.target

     [Service]
     Type=idle
     ExecStart=/usr/bin/python3 /usr/local/bin/MotionDetectDisplayControl.py > /home/pi/motiondetect.log 2>&1

     [Install]
     WantedBy=multi-user.target'
  * commands:
    * 'sudo chmod 644 /lib/systemd/system/motiondetect.service'
    * 'sudo systemctl daemon-reload'
    * 'sudo systemctl enable motion detect.service'

* **bin/display-photos.sh** uses qiv to display photos
  * to start up in x, add the following to */etc/xdg/lxsession/LXDE-pi/autostart*:
    '@/usr/local/bin/display-photos.sh'

* **bin/refresh-gphotos.sh** uses rclone to pull images from a google photos album
  * add this via crontab:
    '0 1 * * * /usr/local/bin/refresh-gphotos.sh'

## Notes & References
* https://drjohnstechtalk.com/blog/2019/08/raspberry-pi-photo-frame-using-your-pictures-on-your-google-drive/

* **rclone**
  * https://rclone.org/install/
  * https://rclone.org/remote_setup/
  * https://rclone.org/googlephotos/
  
* Turn off screen
  * cec control
    * https://www.linuxuprising.com/2019/07/raspberry-pi-power-on-off-tv-connected.html
    * Doesn’t look like Dell monitor shows up
  * xset 
    * Just blanks the screen, Dell monitor still has backlight on 
    * https://askubuntu.com/questions/62858/turn-off-monitor-using-command-line
  * tvservice
    * https://www.raspberrypi.org/forums/viewtopic.php?t=7570
    * tvservice -o  # turn off
    * tvservice -p  # turn on
    * Turn on also needs to “refresh x”:
      * sudo chvt 6
      * sudo chvt 7

* Run at startup
  * https://www.tomshardware.com/how-to/run-script-at-boot-raspberry-pi
  * https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
  * 

## Look into...
* Simple http server
  * https://gist.githubusercontent.com/UniIsland/3346170/raw/059aca1d510c615df3d9fedafabac4d538ebe352/SimpleHTTPServerWithUpload.py

* Pi3d
  * https://www.thedigitalpictureframe.com/pi3d-parameters-directory-config/
  * https://github.com/pi3d/pi3d_demos/blob/master/PictureFrame2020config.py
  * https://github.com/pi3d/pi3d_demos/blob/master/PictureFrame.py#L332
  * https://pi3d.github.io/html/ReadMe.html#demos-on-github-com-pi3d-pi3d-demos-include
  * https://www.thedigitalpictureframe.com/how-to-set-up-your-raspberry-pi-for-your-digital-picture-frame/
  * https://www.thedigitalpictureframe.com/pi3d-parameters-directory-config/

