#!/usr/bin/python

import sys
import subprocess
import re

APP_NAME = 'mediainfo'

if len(sys.argv) < 2:
    print 'Shows media info about input file.\n Usage:', APP_NAME, '<media file>'
    sys.exit()

infile = sys.argv[1]


def get_frames(infile):
    args = ['ffmpeg', '-i', infile]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    pattern1 = re.compile(r'Duration: (\d\d):(\d\d):(\d\d)')
    match = pattern1.search(stderr)
    hours = int(match.groups()[0])
    minutes = int(match.groups()[1])
    seconds = int(match.groups()[2])
    total_seconds = hours * 3600 + minutes * 60 + seconds

    pattern2 = re.compile(r'Stream #0.*?(\d+(?:\.\d+))')
    match = pattern2.search(stderr)
    fps = float(match.groups()[0])

    return total_seconds * fps

frames = get_frames(infile)
print frames