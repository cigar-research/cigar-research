import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import imageio
import os
from skimage import color, io
import skimage
from importlib import reload
from matplotlib import rc
import cv2

import tomo_data

# data_dir = "/Users/jesse/Data/SOC/2018-02-16 Tomografie/data"
# photo_dir = "/Users/jesse/Data/SOC/2018-02-16 Tomografie/gesorteerd"






def compose(f1, f2):
    return lambda x: f1(f2(x))


# cache circular kernels for performance
kernels = {}
def get_circular_kernel(size):
    if size in kernels:
        return kernels[size]
    xs, ys = np.meshgrid(np.arange(size), np.arange(size))
    xs -= ((size - 1) // 2)
    ys -= ((size - 1) // 2)
    rs = xs ** 2 + ys ** 2

    kernel = np.array((rs <= ((size - 1) / 2) ** 2) * 1, dtype=np.uint8)
    kernels[size] = kernel
    return kernel


def get_valid_photo_ids():
    photo_ids = []
    for plak in range(30):
        for kant in ['a', 'v']:
            for poging in range(9):
                photo_id = (plak, kant, poging)
                fname = tomo_data.photo_orig_fn_format % photo_id
                if os.path.isfile(fname):
                    photo_ids.append(photo_id)
    return photo_ids


def generate_cutout(ph_id, th, closing_size, opening_size, th_below=True):
    edited_img = io.imread(tomo_data.photo_edited_fn_format % ph_id)[::-1, :, :]
    orig_img = io.imread(tomo_data.photo_orig_fn_format % ph_id)[::-1, :, :]
    gscale_img = color.rgb2gray(edited_img)
    red_img = edited_img[:, :, 0]
    grn_img = edited_img[:, :, 1]
    blu_img = edited_img[:, :, 2]

    cutout_layer = blu_img

    _, bin_img = cv2.threshold(skimage.img_as_ubyte(cutout_layer), int(th * 255), 255,
                               cv2.THRESH_BINARY_INV if th_below else cv2.THRESH_BINARY)
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, get_circular_kernel(closing_size))
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, get_circular_kernel(opening_size))

    contour_data = find_largest_contour(bin_img)
    contour_mask = create_mask_from_contour(contour_data, bin_img)

    cutout_image = crop_using_mask(orig_img, contour_mask)

    maxc = np.amax(contour_data[:, 0, :], axis=0) + 1
    minc = np.amin(contour_data[:, 0, :], axis=0)

    cutout_image = cutout_image[minc[1]:maxc[1], minc[0]:maxc[0], :]

    np.savez_compressed(tomo_data.data_fn_format % ph_id,
                        contour_data = contour_data,
                        cutout_image = cutout_image
                        )

    io.imsave(tomo_data.cutout_fn_format % ph_id, cutout_image[::-1,:,:], quality=100)

    return cutout_image


def find_largest_contour(bin_img):
    # Find the largest contour and extract it
    im, contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    maxContour = 0
    for contour in contours:
        contourSize = cv2.contourArea(contour)
        if contourSize > maxContour:
            maxContour = contourSize
            maxContourData = contour

    return maxContourData


def create_mask_from_contour(contour_data, img):
    mask = np.zeros(img.shape[0:2], dtype=np.uint8)
    cv2.fillPoly(mask, [contour_data], 1)
    return mask


def crop_using_mask(img, mask):
    if img.ndim == 3:
        mask = mask[:,:,np.newaxis]
        bg = np.array([255, 255, 255], dtype=np.uint8).reshape(1,1,3)
    else:
        bg = 255

    # cropped image is sum of cutout plus background
    return mask * img + (1 - mask) * bg
