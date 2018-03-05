import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import imageio
import os
from skimage import color, io
import skimage
from importlib import reload
from matplotlib import rc

from PIL import Image

import tomo_data
reload(tomo_data)
import cutout_photos

target_area = 2e6
target_dims = np.array([2500, 2500])

def rescale_image(ph_id):
    pil_img = Image.open(tomo_data.rotated_fn_format % ph_id)
    orig_img = np.array(pil_img)

    layer_sum = np.sum(orig_img, axis=-1)
    bin_img = (layer_sum < (3 * 255)).astype(np.uint8)

    area = np.sum(bin_img.flatten())
    print("area: %d" % area)

    scaling_factor = np.sqrt(target_area / area)
    pre_size = np.array(pil_img.size)
    print(pre_size)

    pil_img = pil_img.resize((pre_size * scaling_factor).astype(np.int), Image.ANTIALIAS)

    post_size = np.array(pil_img.size)
    print(post_size)

    background = Image.new('RGB', tuple(target_dims), (255, 255, 255, 255))
    paste_lower = ((target_dims - post_size) / 2).astype(np.int)
    paste_upper = paste_lower + post_size
    background.paste(pil_img, tuple(paste_lower) + tuple(paste_upper))
    background.save(tomo_data.normed_fn_format % ph_id[1::-1])

    return np.array(background)