import numpy as np
import cv2
from cedar_videos import *
import video_funcs
import matplotlib.pyplot as plt

A_msmts = ["A" + str(i+1) for i in range(6)]
frame_step = 10

for m in A_msmts:
    print("Analysing measurement " + m)
    anchor_vector = (anchor_points[m][1, :] - anchor_points[m][0, :]) / anchor_distance
    anchor_length = np.linalg.norm(anchor_vector)

    vidcap = cv2.VideoCapture(os.path.join(data_dir, valid_measurement_videos[m]))
    frames = int(np.round(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)))
    fps = np.round(vidcap.get(cv2.CAP_PROP_FPS))

    frames = np.arange(0, frames, frame_step)
    data_points = frames.size

    flame_tracked_data = np.zeros((data_points, 5))

    success = True
    i = 0
    for f in frames:
        print("Analysing frame %d ..." % f, end=' ')
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, f)
        success, image = vidcap.read()
        if success:
            flame_thresholded_img = video_funcs.get_thresholded_image(image[:, :max_x[m], :])
            # plt.imshow(flame_thresholded_img)

            flame_data = video_funcs.get_flame_data_from_thr_image(flame_thresholded_img, max_x=800,
                                                                   flame_rect_size=np.array([70, 50]))
            if flame_data is not None:
                print("Flame detected")
                flame_center, flame_pixels = flame_data
                # plt.scatter(flame_center[1], flame_center[0])
                # plt.show()
                geo_coord = np.dot(anchor_vector, flame_center[::-1]) / anchor_length ** 2
                flame_tracked_data[i, :] = [f, flame_pixels, flame_center[1], flame_center[0], geo_coord]
                i += 1
            else:
                print("No flame detected")

    flame_tracked_data = flame_tracked_data[:i, :]

    np.savez(os.path.join(data_dir, "analysis", m + ".npz"), flame_tracked_data=flame_tracked_data,
             video_file=valid_measurement_videos[m],
             frames=frames,
             fps=fps
             )