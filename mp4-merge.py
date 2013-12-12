#!/usr/bin/python

import os
import sys
import tempfile
import shutil
import logging

APP_NAME = 'mp4-merge'

if len(sys.argv) < 2:
    print 'Merges MP4 files into one MP4 file.\n Usage:', APP_NAME, '<dir with MP4 files>'
    sys.exit()

indir = sys.argv[1]

INPUT_EXT1 = '.MP4'
OUT_EXT1 = '.mpg'
MP4_RESULT_FILE = 'out.mp4'
VIDEO_QUALITY = 22 #22=10300 Kbps, 23=, 24=6000 Kbps


log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(APP_NAME + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
lfh.setFormatter(formatter)
log.addHandler(lfh)

tmpdir = tempfile.mkdtemp()
log.info('Temp dir ' + tmpdir)

log.info('MP4s -> MPGs')
mpg_file_list = list()
for infile in os.listdir(indir):
    if infile.upper().endswith(INPUT_EXT1):
        outfile = tmpdir + '/' + infile + OUT_EXT1
        cmd = 'ffmpeg -i ' + infile + ' -qscale:v 1 ' + outfile
        log.info(cmd)
        os.system(cmd)
        mpg_file_list.append(outfile)


log.info('MPGs -> MP4')
mpg_files_str = ''
for mpg_file in mpg_file_list:
    mpg_files_str = mpg_files_str + mpg_file + '|'

cmd = 'ffmpeg -i concat:"' + mpg_files_str + '" -c:v libx264 -preset slow -crf ' + str(VIDEO_QUALITY) + ' -c:a aac -strict -2 ' + MP4_RESULT_FILE
log.info(cmd)
os.system(cmd)


log.info('Removing temp dir ' + tmpdir + '...')
shutil.rmtree(tmpdir)
log.info('DONE')
