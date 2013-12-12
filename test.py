#!/usr/bin/python

import sys
import mediainfo

infile = sys.argv[1]
print 'file', infile

frames = mediainfo.get_frames(infile)
print 'frames', frames

fps = mediainfo.get_fps(infile)
print 'fps', fps

lenght = mediainfo.get_length_str(frames, fps)
print 'lenght', lenght

#frames 2817.18
#time 00:01:34