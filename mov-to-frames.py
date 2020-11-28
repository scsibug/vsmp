#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, time, sys, random 
from PIL import Image
import ffmpeg
import re
import sys
import time
import tempfile

def get_framerate(stream):
    fr = stream['avg_frame_rate']
    print(fr)
    fr_comp = re.match("(?P<x>\d+)/(?P<y>\d+)",fr)
    if fr_comp:
        x = fr_comp.group('x')
        y = fr_comp.group('y')
        return (int(x)/int(y))
    else:
        return None

def get_video_stream(filename):
    streams = ffmpeg.probe(filename)['streams']
    for s in streams:
        if s['codec_type']=='video':
            return s

def get_dimensions(stream):
    width = int(stream['width'])
    height = int(stream['height'])
    return (width, height)

def generate_frame(in_filename, out_filename, time, width, height, scale_height):
    s_w = width
    s_h = -1
    if scale_height:
        s_h = height
        s_w = -1
    (
    ffmpeg
    .input(in_filename, ss=time)
    .filter('scale', s_w, s_h)
    .filter('pad',width,height,-1,-1) # could add 'white' argument for white bars
    .output(out_filename, vframes=1)
    .overwrite_output()
    .run(capture_stdout=True, capture_stderr=True)
    )
    
def framecount_to_ms(framerate, fc):
    return fc*(1000/framerate)

def ms_to_timecode(ms):
    return "%dms"%ms

input_vid = sys.argv[1] # Video file
dest_dir = sys.argv[2] # Output PNG directory
start_time = sys.argv[3] # in seconds
end_time = sys.argv[4] # in seconds

vid_stream = get_video_stream(input_vid)
framerate = get_framerate(vid_stream)
vid_dim = get_dimensions(vid_stream)
print("Video Dimensions: {}".format(get_dimensions(vid_stream)))
print("Video Framerate: {}".format(framerate))

# Output screen size
width = 800 
height = 480

# desired output ratio is
output_ratio = width / height
# source ratio is
source_ratio = vid_dim[0] / vid_dim[1]

scale_height = True
if source_ratio > output_ratio:
    scale_height = False

frames_processed = 0
process_start_time = time.time()

# Calculate starting/ending frame number
start_frame = int(round(int(start_time) * framerate,0))
end_frame = int(round(int(end_time) * framerate,0))

for f in range(start_frame, end_frame):
    tf = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    filename = tf.name
    msTimecode = ms_to_timecode(framecount_to_ms(framerate, f))
    generate_frame(input_vid, filename, msTimecode, width, height, scale_height)
    if (not os.path.exists(filename)):
        print("Frame does not exist - may have reached end of input file")
        exit(1)
    pil_im = Image.open(filename)
    pil_im = pil_im.convert(mode='1',dither=Image.FLOYDSTEINBERG)
    with open("{}/{:08d}_bw.png".format(dest_dir,f), 'wb') as output_file:
        pil_im.save(output_file, format="png", optimize=True)
    frames_processed = frames_processed + 1
    working_time = time.time()-process_start_time
    print("Processed {} seconds ({} frames) at {} fps".format(
        round(frames_processed/framerate,1),
        frames_processed,
        round(frames_processed/working_time,1)))
    os.remove(filename)
exit()
