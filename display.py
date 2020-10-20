# EPaper / Image Processing
from waveshare_epd import epd7in5_V2
from PIL import Image

import configparser
import logging
import sys
import time
import glob
import os
from pathlib import Path
    
def playback_settings(framecount, days, sleep_sec):
    """Determine how many frames to skip based on days for total movie
       playtime and sleep time between screen refreshes.
       Returns tuple of (sec-to-sleep, frames-to-skip)
    """
    sec_to_play = days * 24 * 60 * 60
    frames_to_display = sec_to_play / sleep_sec
    frames_to_skip = framecount / frames_to_display
    adjusted_sleep_sec = sleep_sec
    # If there aren't enough frames to last 'days',
    # determine how long we should sleep in order to
    # stretch it out.
    if frames_to_skip < 1:
        adjusted_sleep_sec = (sec_to_play / framecount)
        frames_to_skip = 0
    return (adjusted_sleep_sec, frames_to_skip)

logger = logging.getLogger("vsmp")
#logger.setLevel(logging.INFO)
#streamHandler = logging.StreamHandler()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#streamHandler.setFormatter(formatter)
#logger.addHandler(streamHandler)

logger.info("VSMP Starting Up...")
logger.info("Reading vsmp.config")
config = configparser.ConfigParser()
config.read('vsmp.config')
video_config = config['VIDEO']
image_dir = video_config['FileDirectory']
# TODO: make sure this is a valid directory, with > 0 files
image_files = list(map(os.path.basename, glob.glob(image_dir+'/*.png')))
image_file_count = len(image_files)
runtime_days = int(video_config['RuntimeDays'])
sleep_min = int(video_config['ScreenSleepMinutes'])
curr_frame_file = video_config['FrameCounterFile']
# Compute how long to display an image in seconds.
(sec_to_sleep, frames_to_skip) = playback_settings(image_file_count, runtime_days, sleep_min*60)

epd = epd7in5_V2.EPD()
logger.info("Initing...")
epd.init()
logger.info("Clear screen...")
epd.Clear()
logger.info("Finding Images...")

# Check if there is a current frame

logger.info(image_files)

if curr_frame_file:
    curr_frame = Path(curr_frame_file).read_text()
    curr_frame = curr_frame.replace('\n', '')
    logger.info("Current frame is {}, attempting resume...".format(curr_frame))
    if curr_frame in image_files:
        index = image_files.index(curr_frame)
        logger.info("Frame located, skipping {} frames".format(str(index)))
        image_files = image_files[index:]
    else:
        logger.warning("Frame not found, starting movie over")

for img in image_files:
    logger.info(img)
    # Open the saved frame in PIL
    pil_im = Image.open(image_dir+"/"+img)
    # Write as current frame
    curr_frame = Path(curr_frame_file).write_text(img)
    # display the image
    epd.display(epd.getbuffer(pil_im))
    logger.info("sleeping...")
    # Exit for now to make testing easier
    exit()
    time.sleep(30)
epd.sleep()
epd7in5.epdconfig.module_exit()
exit()    
