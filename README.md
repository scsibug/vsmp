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

This very-slow-movie-player does a few things above what I've seen elsewhere, which are described below.  This project contains scripts to preprocess movie files into image files, select a meaningful subset of frames, and then display on an e-Paper display with configurable total and refresh times.  Movies played through this project are not played at a constant speed (although enough information is preserved to achieve this) - instead, minimizing screen refreshes needed to show meaningfully changed frames on a regular basis is prioritized.

### Offline Image Processing
All image processing is done offline, which lets one comfortably use a small device like the Pi Zero, without running into performance issues.  This also reduces the storage required on the device itself.  A much larger selection of videos can be pre-loaded, or smaller memory cards can be used.  This processing may take significant time, even on powerful desktop machines, so it is not recommended to run this on a low-power device like a Pi Zero - especially when experimenting with different settings.

### Frame Similarity Detection
The refresh time on these e-Paper displays is significant (5-10 seconds), so avoiding useless screen refreshes is important (all black to all black, for example).  Frame-to-frame differences can be calculated, and frames that do not have significant changes can be ignored.

### Runtime and Refresh Time Control
Controls for overall run time and time between refreshes, even after the movie has been processed into images, gives flexibility to the display.

### Autostart and Checkpointing
Finally, autostart functionality through systemd services, and checkpointing to disk allows this to be a set-and-forget solution that does not need to be adjusted after being installed and powered up.

## Walkthrough

### Frame Extraction

Begin by selecting a movie file to process.  The script `mov-to-frames.py` will convert a movie into a directory of PNG frames, given two user-specified timecodes (in seconds).  For example, to generate frames for minute 2 (120 seconds) to minute 125 (7500 seconds), saving the result into the `frames` directory, use this command:

```
$ mkdir frames
$ python3 mov-to-frames.py movie.mp4 frames 120 7500
```

This results in downsampled frames (`800x480` is hardcoded in the script), that have been converted to black and white (with Floyd-Steinberg dithering) PNG images.

### Structural Similarity

Instead of storing and displaying every frame, frames that represent minimal change can be discarded using `compare.py`.  Frames that are sufficiently unique are copied to a new destination directory, run as follows:

```
$ mkdir unique_frames
$ python3 compare.py frames unique_frames 0.99
```

The list of frames is iterated, and each new frame that has less than 99% similarity with the previous saved frame (starting from the first) is saved into the `unique_frames` directory.  The structural similarity algorithm from `scikit-image` is used for this calculation.  There is currently commented-out code in this script that allows for additional debugging - displaying red-tinted "dissimilar" frames, as well as heatmaps of which portions of the frame have changed.

### Displaying on e-Paper

With a directory of relatively unique image frames, these can now be displayed to e-Paper with `display.py`.  A configuration file (sample in `vsmp.config.example`) named `vsmp.config` is read from the current working directory, to determine where image frames are located, how long between screen refreshes, and the total length of runtime desired.  A current frame counter file is specified, which holds the most recently displayed frame.  Each time the program starts, this file is consulted if it exists, and playback is resumed from that point.

Be sure to copy the directory of unique frames to the Raspberry Pi device, customize the config file, and then simply run the script.

### Scheduling for Autorun

The systemd service file `vsmp.service` provides an example of how the `display.py` script can be run automatically on system startup.  Install and enable this like any systemd service.

```
# cp vsmp.service /etc/systemd/system/
# systemctl enable vsmp.service
# systemctl start vsmp.service
```