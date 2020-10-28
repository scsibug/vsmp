import sys, os
import shutil
from skimage.transform import resize
from imageio import imread, imwrite

#from transforms import RGBTransform
# See https://gist.github.com/wchargin/d8eb0cbafc4d4479d004

from skimage.metrics import structural_similarity
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

cmp_size = 100

# similarity below this value results in a new keyframe
# Suggest no less than 0.9 for anime

image_dir = sys.argv[1]
dest_dir = sys.argv[2]
if len(sys.argv)>3:
    key_frame_min_sim = float(sys.argv[3])
else:
    key_frame_min_sim = 0.99

prev_image_name = ""
prev_image = ""

# Combine two approaches
# Compare image pairs. (cmp)
# 00 vs 01, 01 vs 02, etc.
# Record deltas for each frame and the prior.

# Another approach (keyframe)
# Read a frame.  compare subsequent frames,
# until some threshold is reached

def mkframe(f):
    '''Frame data based on the frame count'''
    file_name = this_image_name = "{:08d}_bw.png".format(f)
    file_path =  "{}/{}".format(image_dir,this_image_name)
    if (not os.path.exists(file_path)):
        return None
    img = resize(imread(file_path), (cmp_size, cmp_size))
    return {'frame': f, 'name': file_name, 'path': file_path, 'img': img}

prior_frame = None
key_frame = None
frame_count = 0
key_count = 0
for f in range(0,10000):
    frame_count += 1
    frame = mkframe(f)
    if (prior_frame==None):
        prior_frame = frame
        key_frame = frame
        continue
    if (frame==None or prior_frame==None):
        print("Could not read frame, exiting")
        exit(1)
        
    #prior_score, ssim = structural_similarity(prior_frame['img'], frame['img'], full=True)
    #prior_score_rnd = round(prior_score,3)
    key_score, ssim = structural_similarity(key_frame['img'], frame['img'], full=True)
    key_score_rnd = round(key_score,3)

    # Move keyframes into destination directory
    if (key_score < key_frame_min_sim):
        key_count += 1
        shutil.copy(frame['path'], "{}/{}".format(dest_dir, frame['name']))
        # Tint image red for debugging
        #dest_path = "{}/{}".format(dest_dir, frame['name'])
        #i = Image.open(frame['path'])
        #i_rgb = i.convert('RGB')
        #i_red = RGBTransform().mix_with((255,0,0),factor=0.3).applied_to(i_rgb)
        #i_red.save(dest_path)
        key_frame = frame
    #else:
    #    shutil.copy(frame['path'], "{}/{}".format(dest_dir, frame['name']))

    prior_frame = frame
    print("keyframes: {}/{}, ({:.2f}%)".format(key_count, frame_count, 100*key_count/(frame_count+1)))
    #plt.imshow(ssim,aspect="auto")
    #plt.savefig("{:08d}_diff.png".format(f))
    #prev_image_name = this_image_name
    #prev_image = this_image


