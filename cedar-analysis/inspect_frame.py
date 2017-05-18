import numpy as np
import cv2
from cedar_videos import *
import matplotlib.pyplot as plt

class Formatter(object):
    def __init__(self, im):
        self.im = im
    def __call__(self, x, y):
        z = self.im.get_array()[int(y), int(x)]
        return "x={:.01f}, y={:.01f}".format(x, y)

measurement = "A6"

frame_offset = 300
vidcap = cv2.VideoCapture(os.path.join(data_dir, valid_measurement_videos[measurement]))
vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_offset)

success, image = vidcap.read()

fig, ax = plt.subplots()
im = ax.imshow(image, interpolation='none')
# ax.format_coord = Formatter(im)
plt.show()