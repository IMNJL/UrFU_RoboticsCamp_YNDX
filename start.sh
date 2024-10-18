#!/bin/sh

sleep 3
sudo python /home/pi/work/python_src/xr_startmain.py &
sleep 5
sudo node /home/pi/work/XiaoRGeekBle/code/XiaoRGeek/main.js &
exit 0



