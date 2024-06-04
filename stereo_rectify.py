import cv2
import os
import json
import numpy as np


def rectify(frame_parameter_path, left_raw, right_raw):
    with open(frame_parameter_path) as para_json_file:
        data = json.load(para_json_file)
        camera_parameter = data['camera-calibration']

        l_camera_matrix = np.array(camera_parameter['KL'])
        r_camera_matrix = np.array(camera_parameter['KR'])
        l_dist_coeff = np.array(camera_parameter['DL'])
        r_dist_coeff = np.array(camera_parameter['DR'])
        rotation = np.array(camera_parameter['R'])
        translation = np.reshape(np.array(camera_parameter['T']),(3,1))

        img_size = left_raw.shape[1::-1]
        print(img_size)


        R1, R2, P1, P2, Q, ROI_l, ROI_r = cv2.stereoRectify(l_camera_matrix, l_dist_coeff, r_camera_matrix, r_dist_coeff, img_size, rotation, translation)

        mapLx, mapLy = cv2.initUndistortRectifyMap(l_camera_matrix, l_dist_coeff, R1, P1, img_size, cv2.CV_32F)
        mapRx, mapRy = cv2.initUndistortRectifyMap(r_camera_matrix, r_dist_coeff, R2, P2, img_size, cv2.CV_32F)

        print('map shape:' + str(mapLx.shape) + str(mapLy.shape))

        left_finalpass = cv2.remap(left_raw, mapLx, mapLy, cv2.INTER_LINEAR)
        right_finalpass = cv2.remap(right_raw,mapRx, mapRy, cv2.INTER_LINEAR)

        return left_finalpass, right_finalpass, Q


def save_Q(Q, reprojection_path):
    data = {'reprojection-matrix': Q.tolist()}
    with open(reprojection_path, 'w') as outfile:
        json.dump(data, outfile, separators=(',', ':'), sort_keys=True, indent=4)

def save_finalpass(left_img, right_img, left_path, right_path):
    cv2.imwrite(left_path, left_img)
    cv2.imwrite(right_path, right_img)


def stereo_rectify(rootpath):
    keyframe_list = [os.path.join(rootpath, kf) for kf in os.listdir(rootpath) if ('keyframe' in kf and 'ignore' not in kf)]
    for kf in keyframe_list:
        left_raw_filepath = kf + '/data/left'
        right_raw_filepath = kf + '/data/right'
        frame_para_filepath =kf + '/data/frame_data'
        os.makedirs(kf + '/data/left_finalpass', exist_ok=True)
        os.makedirs(kf + '/data/right_finalpass', exist_ok=True)
        os.makedirs(kf + '/data/reprojection_data', exist_ok=True)
        
        img_filelist = [sf for sf in os.listdir(left_raw_filepath) if '.png' in sf]
        for sf in img_filelist:
            # stereo rectify
            left_raw_file = os.path.join(left_raw_filepath, sf)
            right_raw_file = os.path.join(right_raw_filepath, sf)
            filename, ext = os.path.splitext(sf)
            frame_para_file = os.path.join(frame_para_filepath, filename + '.json')

            left_raw = cv2.imread(left_raw_file)
            right_raw = cv2.imread(right_raw_file)
            print(frame_para_file)
            left_finalpass, right_finalpass, Q = rectify(frame_para_file, left_raw, right_raw)


            # save final pass image and reprojection matrix
            left_finalpass_savefile = kf + '/data/left_finalpass/' + sf
            right_finalpass_savefile = kf + '/data/right_finalpass/' + sf
            reprojection_file = kf + '/data/reprojection_data/' + filename + '.json'
            save_finalpass(left_finalpass, right_finalpass, left_finalpass_savefile, right_finalpass_savefile)
            save_Q(Q, reprojection_file)
