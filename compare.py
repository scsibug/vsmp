import sys, os
import shutil
from skimage.transform import resize
from imageio import imread
from skimage.metrics import structural_similarity

import numpy as np
import matplotlib.pyplot as plt

cmp_size = 100

image_dir = sys.argv[1]
dest_dir = sys.argv[2]

prev_image_name = ""
prev_image = ""
for f in range(0,10000):
    this_image_name = "{:08d}_bw.png".format(f)
    this_image = "{}/{}".format(image_dir,this_image_name)
    # For the first image, skip
    if (f==0):
        prev_image_name = this_image_name
        prev_image = this_image
        continue
    if (not os.path.exists(this_image)):
        exit(1)
    img_a = resize(imread(prev_image), (cmp_size, cmp_size))
    img_b = resize(imread(this_image), (cmp_size, cmp_size))
    score, ssim = structural_similarity(img_a, img_b, full=True)
    if score<0.995:
        print("Keeping unique image with score: {}".format(score))
    else:
        shutil.copy(prev_image, "{}/{}".format(dest_dir, prev_image_name))
        shutil.copy(this_image, "{}/{}".format(dest_dir, prev_image_name))
    plt.imshow(ssim,aspect="auto")
    plt.savefig("{:08d}_diff.png".format(f))
    prev_image_name = this_image_name
    prev_image = this_image


