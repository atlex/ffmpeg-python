#!/usr/bin/python

import os
import sys
import tempfile
import shutil
import logging

APP_NAME = 'qstar-video'

if len(sys.argv) < 3:
    print 'Creates a video from MP4 file.\n Usage:', APP_NAME, '<MP4> <video length in seconds>'
    sys.exit()

infile = sys.argv[1]
seconds = sys.argv[2]
frames = seconds * 30

START_IMG = 'start.png'
RESULT_FILE = 'out.mp4'

log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(APP_NAME + '.log')
log.addHandler(lfh)

tmpdir = tempfile.mkdtemp()
log.info('Temp dir ' + tmpdir + ' is created.')

#1 video with fade from PNG
outfile1 = tmpdir + '/1.mpg'
cmd = 'ffmpeg -loop 1 -f image2 -i ' + START_IMG + ' -t 5 -f lavfi -i aevalsrc=0 -vf "fade=in:0:25,fade=out:110:25" -r 29.97 -qscale:v 1 ' + outfile1
os.system(cmd)

#2 video with fade
outfile2 = tmpdir + '/2.mpg'
start_end_frame = frames - 50;
cmd = 'ffmpeg -i ' + infile + ' -qscale:v 1 -vf "fade=in:0:50,fade=out:' + start_end_frame + ':50" ' + outfile2
os.system(cmd)

#Merge 1 and 2 videos
outmpg = tmpdir + '/out.mpg'
cmd = 'ffmpeg -i concat:"' + outfile1 + '|' + outfile2 + '" -c copy ' + outmpg
os.system(cmd)

#Compress MPG -> MP4
cmd = 'ffmpeg -i ' + outmpg + ' -c:v libx264 -preset slow -crf 23 -c:a aac -strict -2 ' + RESULT_FILE
os.system(cmd)

#Clean
log.info('Removing temp dir ' + tmpdir + '...')
shutil.rmtree(tmpdir)
log.info('DONE')

