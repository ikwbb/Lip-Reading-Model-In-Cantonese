import sys
sys.path.insert(0, "./auto_avsr")

import os
import torch
import torchvision
import cv2
from tqdm import tqdm
import argparse

from preparation.data.data_module import AVSRDataLoader

class AVSRDataLoader(torch.nn.Module):
    def __init__(self, detector="retinaface"):
        super().__init__()
        if detector == "retinaface":
            from preparation.detectors.retinaface.detector import LandmarksDetector
            from preparation.detectors.retinaface.video_process import VideoProcess
            self.landmarks_detector = LandmarksDetector(device="cuda:0")
            self.video_process = VideoProcess(convert_gray=False)

    def forward(self, data_filename):
        video = self.load_video(data_filename)
        landmarks, multi_face_detected = self.landmarks_detector(video)
        video = self.video_process(video, landmarks)
        video = torch.tensor(video)
        return video, multi_face_detected

    def load_video(self, data_filename):
        return torchvision.io.read_video(data_filename, pts_unit="sec")[0].numpy()

video_dataloader = AVSRDataLoader(detector="retinaface")

def save2vid(filename, vid, frames_per_second):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    torchvision.io.write_video(filename, vid, frames_per_second)

def get_video_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return int(fps) if fps > 0 else 50

def process_videos(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    video_files = [f for f in os.listdir(input_dir) if f.endswith(".mp4")]
    failed_videos = []

    with tqdm(total=len(video_files), desc="Processing Videos") as pbar:
        for filename in video_files:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            if os.path.exists(output_path):
                print(f"Already processed: {filename}, skipping...")
                os.remove(input_path)
                pbar.update(1)
                continue

            try:
                fps = get_video_fps(input_path)
                preprocessed_video, multi_face_detected = video_dataloader(input_path)
                
                if multi_face_detected:
                    print(f"Skip: {filename}")
                else:
                    save2vid(output_path, preprocessed_video, frames_per_second=fps)
            except Exception as e:
                failed_videos.append(filename)
                print(f"Error processing {filename}: {str(e)}")
                
            os.remove(input_path)
            pbar.update(1)

    print("Processing complete!")
    if failed_videos:
        print("Failed videos:", failed_videos)


input_dir = './icable_sliced/'
output_dir = "./icable_preprocessed/"
process_videos(input_dir, output_dir)