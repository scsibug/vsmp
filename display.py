# EPaper / Image Processing
from waveshare_epd import epd7in5_V2
from PIL import Image

# AWS IoT
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

import configparser
import logging
import sys
import time
import glob

awslogger = logging.getLogger("AWSIoTPythonSDK.core")
awslogger.setLevel(logging.INFO)
logger = logging.getLogger("vsmp")
logger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
awslogger.addHandler(streamHandler)
logger.addHandler(streamHandler)

logger.info("VSMP Starting Up...")
logger.info("Reading vsmp.config")


epd = epd7in5_V2.EPD()
logger.info("Initing...")
epd.init()
logger.info("Clearing screen...")
epd.Clear()
logger.info("Finding Images...")
image_dir = sys.argv[1]
skipcount = 0
inwork = 0
for img in sorted(glob.glob(image_dir+'/*.png')):
    inwork=+1
    if inwork < skipcount:
        continue
    logger.info(img)
    # Open the saved frame in PIL
    pil_im = Image.open(img)
    # display the image
    epd.display(epd.getbuffer(pil_im))
    time.sleep(30)
epd.sleep()
epd7in5.epdconfig.module_exit()
exit()    
