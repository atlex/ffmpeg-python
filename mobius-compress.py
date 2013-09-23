#!/usr/bin/python

import os
import sys

APP_NAME = 'mobius-compress'

#22
#26 
#27 4500Kbps
DEFAULT_VIDEO_QUALITY = 26 

if len(sys.argv) < 2:
    print 'Compresses MP4 file into smaller MP4 file.\n Usage:', APP_NAME, '<MP4> [secs]'
    sys.exit()

infile = sys.argv[1]
name, ext = os.path.splitext(infile)
outfile = name + '_compressed.mp4'

video_quality = DEFAULT_VIDEO_QUALITY
#if len(sys.argv) > 2:    
#    video_quality = sys.argv[2]

time = ''
if len(sys.argv) > 2:
    secs = sys.argv[2]
    time = '-ss 00:00:00 -t 00:00:' + secs



cmd = 'ffmpeg -i ' + infile + ' -c:v  libx264 -preset slow -crf '+ str(video_quality) + ' -c:a copy ' + time + ' ' + outfile
os.system(cmd)