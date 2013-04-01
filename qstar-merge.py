#!/usr/bin/python

import os
import sys
import tempfile
import shutil
import logging

APP_NAME = 'qstar-merge'

if len(sys.argv) < 2:
    print 'Merges MOV files into one MP4 file.\n Usage:', APP_NAME, '<dir with MOV files>'
    sys.exit()

indir = sys.argv[1]

log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(indir + '/' + APP_NAME + '.log')
#lfh.setLevel(logging.DEBUG)
log.addHandler(lfh)

tmpdir = tempfile.mkdtemp()
log.info('Created temp dir ' + tmpdir + '.')

INPUT_EXT1 = '.MOV'
OUT_EXT1 = '.mp4'
INPUT_EXT2 = INPUT_EXT1 + OUT_EXT1 #.MOV.mp4
OUT_EXT2 = '.ts'
RESULT_FILE = indir + '/out.mp4'

log.info('### MOV -> MP4')
for infile in os.listdir(indir):
    if infile.endswith(INPUT_EXT1):
        #log.info(infile)
        outfile = tmpdir + '/' + infile + OUT_EXT1
        cmd = 'ffmpeg -i ' + infile + ' -c:v copy -c:a aac -strict -2 -b:a 96k ' + outfile
        os.system(cmd)
        log.info(outfile)

log.info('### MP4 -> TS')
for infile in os.listdir(tmpdir):
    if infile.endswith(INPUT_EXT2):
        infile = tmpdir + '/' + infile
        #log.info(infile)
        outfile = infile + OUT_EXT2
        cmd = 'ffmpeg -i ' + infile + ' -c copy -vbsf h264_mp4toannexb ' + outfile
        os.system(cmd)
        log.info(outfile)

log.info('### TS -> OUT.MP4')
tsfiles = ''
for infile in os.listdir(tmpdir):
    if infile.endswith(OUT_EXT2):
        infile = tmpdir + '/' + infile
        #log.info(infile)
        tsfiles = tsfiles + infile + '|'

cmd = 'ffmpeg -i concat:"' + tsfiles + '" -c copy -absf aac_adtstoasc ' + RESULT_FILE
os.system(cmd)
log.info('RESULT=' + RESULT_FILE)

### Clean
log.info('Removing temp dir ' + tmpdir + '...')
shutil.rmtree(tmpdir)
log.info('DONE')
