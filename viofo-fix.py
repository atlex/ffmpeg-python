#!/usr/bin/python

import os
import sys
import tempfile
import shutil
import logging

APP_NAME = 'viofo-fix'

if len(sys.argv) < 3:
    print 'Fixes Viofo MP4 files.\n Usage:', APP_NAME, '<dir with MP4 files>, <out dir>'
    sys.exit()

indir = sys.argv[1]
outdir = sys.argv[2]

INPUT_EXT1 = '.MP4'
OUT_EXT1 = '.mp4'
VIDEO_QUALITY = '40M'


log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(APP_NAME + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
lfh.setFormatter(formatter)
log.addHandler(lfh)

log.info('Input dir ' + indir)

log.info('Output dir ' + outdir)
os.mkdir(outdir)

for infile in os.listdir(indir):
    if infile.upper().endswith(INPUT_EXT1):
        outfile = outdir + '/' + infile + OUT_EXT1
        cmd = 'ffmpeg -i ' + infile + ' -c:v h264_videotoolbox -b:v ' + VIDEO_QUALITY + ' -c:a copy ' + outfile
        log.info(cmd)
        os.system(cmd)

log.info('DONE')
