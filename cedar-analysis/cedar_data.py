import os
import numpy as np


valid_measurements = []
valid_measurements += ["S" + str(i+1) for i in range(14)]
valid_measurements += ["H" + str(i+1) for i in range(8)]
valid_measurements += ["HE" + str(i+1) for i in range(2)]
valid_measurements += ["A" + str(i+1) for i in range(6)]

valid_measurement_videos = {}

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

flame_velocities = {'A2': 0.25613843857418367, 'A4': 0.29279065764664025, 'A5': 0.45823729028041699, 'A3': 0.31790309144223566, 'A6': 0.67456949486780737, 'A1': 0.20350405996497073}
avg_flame_sizes = {'A2': 0.41151763096332444, 'A4': 0.45183719977299375, 'A5': 0.57490772344488039, 'A3': 0.49398170378084438, 'A6': 0.72366521729190791, 'A1': 0.17852154073069088}
local_data_dir = "data"
SBG_data_file = os.path.join(local_data_dir, "SBG_data_all.dat")

SBG_records_splits = np.array([0, 8077,  8176,  9612, 11934, 16389, 18428, 21077, 22953, 33266,
       35553, 37708, 40328, 42355, 44476, 46781, 49747, 52133, 54116,
       56344, 59193, 61582, 63864, 65968, 68121, 71621])

SBG_data_indices = {
    "S1": 0,
    "S2": 2,
    "S3": 3,
    "S4": 4,
    "S5": 5,
    "S6": 6,
    "S7": 7,
    "S8": 8,
    "S9": 9,
    "S10": 10,
    "S11": 11,
    "S12": 12,
    "S13": 13,
    "S14": 14,
    "H1": 15,
    "H2": 16,
    "H3": 17,
    "H4": 18,
    "H5": 19,
    "H6": 20,
    "H7": 21,
    "H8": 22,
    "HE1": 23,
    "HE2": 24
}

SBG_horz_separation = {
    "S1": 2.5,
    "S2": 2.5,
    "S3": 2.5,
    "S4": 2.5,
    "S5": 2.5,
    "S6": 2.5,
    "S7": 2.5,
    "S8": 2.5,
    "S9": 2.5,
    "S10": 2.5,
    "S11": 2.5,
    "S12": 2.5,
    "S13": 2.5,
    "S14": 2.5,
    "H1": 2.5,
    "H2": 2.5,
    "H3": 2.5,
    "H4": 2.5,
    "H5": 2.5,
    "H6": 2.5,
    "H7": 2.5,
    "H8": 2.5,
    "HE1": 1.0,
    "HE2": 1.0
}

SBG_vert_separation = {
    "S1": 2.0,
    "S2": 2.0,
    "S3": 2.5,
    "S4": 2.5,
    "S5": 3.0,
    "S6": 3.0,
    "S7": 4.0,
    "S8": 4.0,
    "S9": 7.0,
    "S10": 7.0,
    "S11": 1.5,
    "S12": 0.5,
    "S13": 3.5,
    "S14": 5.5,
    "H1": 0.0,
    "H2": 0.0,
    "H3": 0.5,
    "H4": 1.0,
    "H5": 1.5,
    "H6": 2.0,
    "H7": 2.5,
    "H8": 4.0,
    "HE1": 2.0,
    "HE2": 0.5,
}

SBG_measurements = []

H_msmts = ["S" + str(i+1) for i in range(14)]
S_msmts = ["H" + str(i+1) for i in range(8)]
HE_msmts = ["HE" + str(i+1) for i in range(2)]

SBG_measurements += S_msmts
SBG_measurements += H_msmts
SBG_measurements += HE_msmts