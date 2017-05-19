import os
import numpy as np

from cedar_data import *

data_dir = "../../../Data/SOC/2017-05-16 Cederhout"
data_files = os.listdir(data_dir)
video_files = [file for file in data_files if file.lower().endswith("avi")]

for vm in valid_measurements:
    valid_measurement_videos[vm] = [video for video in video_files if vm.lower() in video.lower()][0]