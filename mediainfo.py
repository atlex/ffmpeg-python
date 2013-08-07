#!/usr/bin/python

import sys
import subprocess
import re
import time

#APP_NAME = 'mediainfo'

# if len(sys.argv) < 2:
#     print 'Shows media info about input file.\n Usage:', APP_NAME, '<media file>'
#     sys.exit()
#
# infile = sys.argv[1]

#Stream #0:0(und): Video: h264 (Baseline) (avc1 / 0x31637661), yuv420p, 1920x1080, 21389 kb/s, 29.97 fps, 29.97 tbr, 600 tbn, 1200 tbc
#Stream #0.*?(\d+(?:\.\d+))

#Stream #0:0(und): Video: h264 (Main) (avc1 / 0x31637661), yuv420p, 1280x720, 4817 kb/s, 14 fps, 14 tbr, 600 tbn, 1200 tbc
#Stream #0.*?(\d+(?:\.\d+)?)\s*fps

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

    pattern2 = re.compile(r'Stream #0.*?(\d+(?:\.\d+)?)\s*fps')
    match = pattern2.search(stderr)
    fps = float(match.groups()[0])

    return total_seconds * fps


def get_fps(infile):
    args = ['ffmpeg', '-i', infile]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    pattern1 = re.compile(r'Stream #0.*?(\d+(?:\.\d+)?)\s*fps')
    match = pattern1.search(stderr)
    fps = float(match.groups()[0])

    return fps


def get_length_str(frames, fps):
    total_seconds = frames / fps
    return time.strftime('%H:%M:%S', time.gmtime(total_seconds))


# frames = get_frames(infile)
# print frames