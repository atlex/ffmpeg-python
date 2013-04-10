#!/usr/bin/python

import os
import sys

APP_NAME = 'png'

if len(sys.argv) < 3:
    print 'Gets one image from a video file.\n Usage:', APP_NAME, '<video> <time>'
    sys.exit()

infile = sys.argv[1]
time = sys.argv[2]

OUT_FILE = 'start.png'

cmd = 'ffmpeg -i '+ infile + ' -vframes 1 -ss  ' + time + ' -f image2 ' + OUT_FILE
os.system(cmd)