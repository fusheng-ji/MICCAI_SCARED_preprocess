import cv2
import os
import numpy as np


def image_sciss(image_file, left_savepath, right_savepath):
    os.makedirs(left_savepath, exist_ok=True)
    os.makedirs(right_savepath, exist_ok=True)
    print('-- current image :' + image_file + " --")
    stacked = cv2.imread(image_file)
    print(stacked.shape)
    left_img = stacked[:1024, :, :]
    right_img = stacked[1024:, :, :]
    path, file = os.path.split(image_file)

    cv2.imwrite(os.path.join(left_savepath, file), left_img)
    cv2.imwrite(os.path.join(right_savepath, file), right_img)




def image_scissor(path):
    rootpath = path
    keyframe_list = [os.path.join(rootpath, kf) for kf in os.listdir(rootpath) if ('keyframe' in kf and 'ignore' not in kf)]
    for kf in keyframe_list:
        stacked_filepath = kf + '/data/rgb_data'
        stacked_filelist = [sf for sf in os.listdir(stacked_filepath) if '.png' in sf]
        for sf in stacked_filelist:
            image_file = os.path.join(stacked_filepath, sf)
            left_savepath = kf + '/data/left'
            right_savepath = kf + '/data/right'
            image_sciss(image_file, left_savepath, right_savepath)



