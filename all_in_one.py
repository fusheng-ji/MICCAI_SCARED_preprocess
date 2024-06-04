from video_parser import video_parser
from image_scissor import image_scissor
from stereo_rectify import stereo_rectify
from depth_to_disp import depth_to_disparity
import os
import glob
from pathlib import Path
import xtarfile as tarfile
from tqdm import trange
if __name__ == "__main__":
    rootpath = '../datasets/scared'
    
    for dataset_dir in sorted(glob.glob(os.path.join(rootpath,'dataset_*'))):
        keyframe_list = os.listdir(dataset_dir)
        for index in trange(len(keyframe_list)):
            keyframe_dir = keyframe_list[index]
            if not os.path.exists(Path(dataset_dir)/keyframe_dir/'data'):
                os.rename(Path(dataset_dir)/keyframe_dir,Path(dataset_dir)/(keyframe_dir+'_ignore'))
            if os.path.exists(Path(dataset_dir)/keyframe_dir/'data'):
                with tarfile.open(os.path.join(dataset_dir,keyframe_dir,'data','scene_points.tar.gz'), 'r') as archive:
                    archive.extractall(os.path.join(dataset_dir,keyframe_dir,'data','scene_points'))
                with tarfile.open(os.path.join(dataset_dir,keyframe_dir,'data','frame_data.tar.gz'), 'r') as archive:
                    archive.extractall(os.path.join(dataset_dir,keyframe_dir,'data','frame_data'))
        video_parser(dataset_dir)

        image_scissor(dataset_dir)

        stereo_rectify(dataset_dir)

        depth_to_disparity(dataset_dir)
