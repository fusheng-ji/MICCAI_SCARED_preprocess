from os import listdir
from os.path import isfile, join, splitext
import cv2
import json
import os

def parse_video(video_file, rgb_filepath):
    os.makedirs(rgb_filepath, exist_ok=True)
    # read video and parse the frame based on stamp_list
    print("--"+ video_file + "  video have been load--")
    vidcap = cv2.VideoCapture(video_file)
    success, frame = vidcap.read()
    count = 0

    while success:
        cv2.imwrite(join(rgb_filepath, 'frame_data%.6d.png' % count), frame)
        print("frame_data%.6d has been saved" % count)
        count += 1
        success, frame = vidcap.read()

        if cv2.waitKey(10) == 27:
            break
    print("total frames: %d" %count)


def video_parser(path):
    rootpath = path

    keyframe_list = [join(rootpath, kf) for kf in listdir(rootpath) if ('keyframe' in kf and 'ignore' not in kf)]
    for kf in keyframe_list:
        video_file = kf + '/data/rgb.mp4'
        rgb_filepath = kf + '/data/rgb_data'

        parse_video(video_file, rgb_filepath)
