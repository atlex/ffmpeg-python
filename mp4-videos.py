#!/usr/bin/python

import os
import sys
import tempfile
import logging
import shutil
import mediainfo

APP_NAME = 'mp4-videos'

if len(sys.argv) < 2:
    print 'Creates a video from MP4 files.\n Usage:', APP_NAME, '<dir with MP4 files>'
    sys.exit()

indir = sys.argv[1]

START_IMG = 'start.png'
INPUT_EXT1 = '.MP4'
OUT_EXT1 = '.mpg'
MP4_RESULT_FILE = 'out.mp4'
FADE_FRAMES = 50
VIDEO_QUALITY = 22 #22=Mbps, 23=Mbps, 24=6Mbps

log = logging.getLogger(APP_NAME)
log.setLevel(logging.DEBUG)
lfh = logging.FileHandler(APP_NAME + '.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
lfh.setFormatter(formatter)
log.addHandler(lfh)

tmpdir = tempfile.mkdtemp()
log.info('Temp dir ' + tmpdir)


log.info('PNG -> MPG')
outfile_start = tmpdir + '/' + START_IMG + OUT_EXT1
cmd = 'ffmpeg -loop 1 -f image2 -i ' + START_IMG + ' -t 5 -f lavfi -i aevalsrc=0 -vf "fade=in:0:25,fade=out:110:25" -r 29.97 -qscale:v 1 ' + outfile_start
log.info(cmd)
os.system(cmd)


log.info('MP4s -> MPGs')
mpg_file_list = list()
mpg_file_list.append(outfile_start)
for infile in os.listdir(indir):
    if infile.upper().endswith(INPUT_EXT1):
        outfile = tmpdir + '/' + infile + OUT_EXT1
        frames = mediainfo.get_frames(infile)
        start_end_frame = frames - FADE_FRAMES
        cmd = 'ffmpeg -i ' + infile + ' -qscale:v 1 -vf "fade=in:0:' + str(FADE_FRAMES) + ',fade=out:' + str(start_end_frame) + ':' + str(FADE_FRAMES) + '" ' + outfile
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
