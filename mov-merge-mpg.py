#!/usr/bin/python

import os
import sys
import tempfile
import shutil
import logging

APP_NAME = 'mov-merge-mpg'

if len(sys.argv) < 2:
    print 'Merges MOV files into one MPG file.\n Usage:', APP_NAME, '<dir with MOV files>'
    sys.exit()

indir = sys.argv[1]

log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(indir + '/' + APP_NAME + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
lfh.setFormatter(formatter)
log.addHandler(lfh)

tmpdir = tempfile.mkdtemp()
log.info('Created temp dir ' + tmpdir + '.')

INPUT_EXT = '.MOV'
#OUT_EXT = '.mpg'
OUT_EXT = '.ts'
RESULT_FILE = indir + '/out' + OUT_EXT

log.info('### MOVs -> MPGs')
for infile in os.listdir(indir):
    if infile.endswith(INPUT_EXT):
        outfile = tmpdir + '/' + infile + OUT_EXT
        #cmd = 'ffmpeg -i ' + infile + ' -qscale:v 1 '  + outfile
        cmd = 'ffmpeg -i ' + infile + ' -c copy -vbsf h264_mp4toannexb '  + outfile
        os.system(cmd)
        log.info(outfile)


log.info('### MPGs -> OUT.MPG')
files = ''
for infile in os.listdir(tmpdir):
    if infile.endswith(OUT_EXT):
        infile = tmpdir + '/' + infile
        files = files + infile + '|'

#cmd = 'ffmpeg -i concat:"' + files + '" -c copy ' + RESULT_FILE
cmd = 'ffmpeg -i concat:"' + files + '" -c copy -absf aac_adtstoasc ' + RESULT_FILE
os.system(cmd)
log.info('RESULT=' + RESULT_FILE)

### Clean
#log.info('Removing temp dir ' + tmpdir + '...')
#shutil.rmtree(tmpdir)
#log.info('DONE')
