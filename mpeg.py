#!/usr/bin/python

import os
import sys
import logging

APP_NAME = 'mpeg'

if len(sys.argv) < 4:
    print 'Creates a MPEG file from a given video file.\n Usage:', APP_NAME, '<video file> <video length in seconds> <fps>'
    sys.exit()

infile = sys.argv[1]
name, ext = os.path.splitext(infile)
outfile = name + '.mpg'
seconds = int(sys.argv[2])
fps = int(sys.argv[3])
frames = seconds * fps

log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(APP_NAME + '.log')
log.addHandler(lfh)

start_end_frame = frames - 50
cmd = 'ffmpeg -i ' + infile + ' -qscale:v 1 -vf "fade=in:0:50,fade=out:' + str(start_end_frame) + ':50" ' + outfile
log.info(cmd)
os.system(cmd)