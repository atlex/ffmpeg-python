#!/usr/bin/python

import os
import sys

APP_NAME = 'qstar-compress'

if len(sys.argv) < 2:
    print 'Compresses MP4 file into enhanced MP4 file.\n Usage:', APP_NAME, '<MP4> <secs>'
    sys.exit()

infile = sys.argv[1]
name, ext = os.path.splitext(infile)
outfile = name + '_compressed.mp4'

time = ''
if len(sys.argv) > 2:
    secs = sys.argv[2]
    time = '-ss 00:00:00 -t 00:00:' + secs

gamma      = '1.0'  # <0.1-10> initial gamma value (default: 1.0)
contrast   = '1.0'  # <-2-2> initial contrast, where negative values result in a negative image (default: 1.0)
brightness = '0.1'  # <-1-1> initial brightness (default: 0.0)
saturation = '1.5'  # <0-3> initial saturation (default: 1.0)

cmd = 'ffmpeg -i ' + infile + ' -c:v  libx264 -preset slow -crf 27 -vf "mp=eq2=' + gamma + ':' + contrast + ':' + brightness + ':' + saturation + '" -c:a copy ' + time + ' ' + outfile
os.system(cmd)