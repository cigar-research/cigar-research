import os
import numpy as np

data_dir = "../../../Data/SOC/2017-05-16 Cederhout"
data_files = os.listdir(data_dir)
video_files = [file for file in data_files if file.lower().endswith("avi")]

valid_measurements = []

valid_measurements += ["S" + str(i+1) for i in range(14)]
valid_measurements += ["H" + str(i+1) for i in range(8)]
valid_measurements += ["HE" + str(i+1) for i in range(2)]
valid_measurements += ["A" + str(i+1) for i in range(6)]

valid_measurement_videos = {}

for vm in valid_measurements:
    valid_measurement_videos[vm] = [video for video in video_files if vm.lower() in video.lower()][0]

anchor_points = {
    "A1": np.array([
        [371, 267],
        [714, 261],
    ]),
    "A2": np.array([
        [355, 422],
        [737, 325]
    ]),
    "A3": np.array([
        [423, 602],
        [767, 397],
    ]),
    "A4": np.array([
        [384, 610],
        [727, 401],
    ]),
    "A5": np.array([
        [459, 666],
        [727, 399],
    ]),
    "A6": np.array([
        [497, 689],
        [684, 360],
    ]),
}

max_x = {
    "A1": 800,
    "A2": 800,
    "A3": 900,
    "A4": 900,
    "A5": 900,
    "A6": 750
}

flame_rect_size = np.array([70, 50])

anchor_distance = 11

valid_time_ranges = {
    "A1": [20, 80],
    "A2": [20, 60],
    "A3": [20, 50],
    "A4": [30, 60],
    "A5": [20, 45],
    "A6": [10, 25]
}

angles = {
    "A1": 90.0,
    "A2": 75.0,
    "A3": 60.0,
    "A4": 60.0,
    "A5": 45.0,
    "A6": 30.0
}

flame_velocities = {'A2': 0.25633279568768552, 'A4': 0.2919549600733029, 'A5': 0.45665004992767705, 'A3': 0.31828854025247422, 'A6': 0.66787749217954384, 'A1': 0.20337500111220155}
