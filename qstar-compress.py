#!/usr/bin/python

import os
import sys

APP_NAME = 'qstar-compress'

if len(sys.argv) < 2:
    print 'Compresses MP4 file into enhanced MP4 file.\n Usage:', APP_NAME, '<MP4> <secs>'
    sys.exit()

infile = sys.argv[1]
outfile = infile + '.mp4'

#ffmpeg -i out.mp4 -c:v libx264 -preset slow -crf 27 -vf "mp=eq2=1.0:1.0:0.1:1.5" -c:a copy -ss 00:00:00 -t 00:00:10 out2.mp4

cmd = 'ffmpeg -i ' + infile + ' -c:v  libx264 -preset slow -crf 27 -vf "mp=eq2=1.0:1.0:0.1:1.5" -c:a copy ' + outfile
os.system(cmd)