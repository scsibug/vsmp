# VSMP
Very Slow Movie Player

Inspired by:
* [How to Build a Very Slow Movie Player for £120 in 2020](https://debugger.medium.com/how-to-build-a-very-slow-movie-player-in-2020-c5745052e4e4) - Tom Whitwell
* [Creating a Very Slow Movie Player](https://medium.com/s/story/very-slow-movie-player-499f76c48b62) - Bryan Boyer

Hardware from:
* [Waveshare](https://www.waveshare.com/) - E-Paper display
  * I have used [7.5inch e-Paper HAT V2](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT), and [7.8inch e-Paper HAT](https://www.waveshare.com/wiki/7.8inch_e-Paper_HAT)
* [RaspberryPi](https://www.raspberrypi.org/) - Pi Zero W
  * Getting some headers is a good idea, for easily connecting the e-Paper HAT.

## Overview and Features

This very-slow-movie-player does a few things above what I've seen elsewhere, which are described below.  This project contains scripts to preprocess movie files into image files, select a meaningful subset of frames, and then display on an e-Paper display with configurable total and refresh times.

### Offline Image Processing
All image processing is done offline, which lets one comfortably use a small device like the Pi Zero, without running into performance issues.  This also reduces the storage required on the device itself.  A much larger selection of videos can be pre-loaded, or smaller memory cards can be used.

### Frame Similarity Detection
The refresh time on these e-Paper displays is significant (5-10 seconds), so avoiding useless screen refreshes is important (all black to all black, for example).  Frame-to-frame differences can be calculated, and frames that do not have significant changes can be ignored.

### Runtime and Refresh Time Control
Controls for overall run time and time between refreshes, even after the movie has been processed into images, gives flexibility to the display.

### Autostart and Checkpointing
Finally, autostart functionality through systemd services, and checkpointing to disk allows this to be a set-and-forget solution that does not need to be adjusted after being installed and powered up.
