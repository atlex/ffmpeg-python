#!/usr/bin/python

import os
import sys
import tempfile
import shutil
import logging
import mediainfo

APP_NAME = 'mp4-video'

if len(sys.argv) < 2:
    print 'Creates a video from MP4 file.\n Usage:', APP_NAME, '<MP4>'
    sys.exit()

infile = sys.argv[1]

START_IMG = 'start.png'
RESULT_FILE = 'out.mp4'
FADE_FRAMES = 50
VIDEO_QUALITY = 22 #22-25

log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(APP_NAME + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
lfh.setFormatter(formatter)
log.addHandler(lfh)


tmpdir = tempfile.mkdtemp()
log.info('Temp dir ' + tmpdir + ' is created.')

log.info('1 MPG with fade from PNG')
outfile1 = tmpdir + '/1.mpg'
cmd = 'ffmpeg -loop 1 -f image2 -i ' + START_IMG + ' -t 5 -f lavfi -i aevalsrc=0 -vf "fade=in:0:25,fade=out:110:25" -r 29.97 -qscale:v 1 ' + outfile1
log.info(cmd)
os.system(cmd)

log.info('2 MPG with fade')
outfile2 = tmpdir + '/2.mpg'
frames = mediainfo.get_frames(infile)
start_end_frame = frames - FADE_FRAMES
cmd = 'ffmpeg -i ' + infile + ' -qscale:v 1 -vf "fade=in:0:' + str(FADE_FRAMES) + ',fade=out:' + str(start_end_frame) + ':' + str(FADE_FRAMES) + '" ' + outfile2
log.info(cmd)
os.system(cmd)

log.info('Merge 1 and 2 MPGs and compress into MP4')
cmd = 'ffmpeg -i concat:"' + outfile1 + '|' + outfile2 + '" -c:v libx264 -preset slow -crf ' + str(VIDEO_QUALITY) + ' -c:a aac -strict -2 ' + RESULT_FILE
log.info(cmd)
os.system(cmd)

#Clean
log.info('Removing temp dir ' + tmpdir + '...')
shutil.rmtree(tmpdir)
log.info('DONE')

