import numpy as np

ths = [200, 210, 240]


def get_thresholded_image(input_img):
    return (input_img[:, :, 0] > ths[0]) & (input_img[:, :, 1] > ths[1]) & (input_img[:, :, 0] > ths[2])


def get_image_centroid_and_pixels(input_img):
    flame_pixels = input_img.sum()
    if flame_pixels > 0:
        return np.argwhere(input_img == 1).sum(0) / flame_pixels, flame_pixels
    else:
        return None


def get_masked_image_centroid_and_pixels(input_img, mask_rect):
    x1, y1, x2, y2 = [int(v) for v in mask_rect]
    cropout_img = input_img[x1:x2, y1:y2]
    flame_data = get_image_centroid_and_pixels(cropout_img)
    if flame_data:
        cropout_centroid, flame_pixels = flame_data
        centroid = cropout_centroid + mask_rect[0:2]
        return centroid, flame_pixels
    else:
        return None


def get_mask_rect(rect_center, rect_size):
    return np.append(rect_center - rect_size / 2, rect_center + rect_size / 2)


def get_flame_data_from_thr_image(input_img, max_x, flame_rect_size=np.array([50, 50])):
    bare_data = get_image_centroid_and_pixels(input_img)
    if bare_data is not None:
        bare_center, _ = bare_data
        flame_data = get_masked_image_centroid_and_pixels(input_img, get_mask_rect(bare_center, flame_rect_size * 2))
        if flame_data:
            masked_center, flame_pixels = flame_data
            return masked_center, flame_pixels
    return None