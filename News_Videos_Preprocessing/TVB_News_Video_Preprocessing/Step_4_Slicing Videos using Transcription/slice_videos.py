import os
import re
from tqdm import tqdm
import subprocess
from concurrent.futures import ThreadPoolExecutor

def parse_srt(filename):
    """Extract SRT files and return start and end times"""
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    pattern = re.compile(r'\d+\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})')
    times = pattern.findall(content)
    return times

def slice_video(video_path, times, output_dir, base_filename, max_workers=4):
    """Using Multiprocessing to slice video segments"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    def cut_segment(index, start, end):
        """Slice a segment (a sentence) of the video"""
        start = start.replace(',', '.')
        end = end.replace(',', '.')
        output_path = os.path.join(output_dir, f"{base_filename}_{index}.mp4")
        command = [
            'ffmpeg', '-y', '-i', video_path, 
            '-ss', start, '-to', end, 
            '-c:v', 'libx264', '-c:a', 'aac', output_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            print(f"Error occurred when processing {output_path}: {result.stderr.decode()}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(cut_segment, index, start, end) 
                   for index, (start, end) in enumerate(times)]
        for future in futures:
            future.result()

def main():
    video_dir = './TVB Reporter Videos'
    srt_dir = './TVB_SRT_Transcribing\\srts'
    output_dir = './TVB_trim\\trimmed_videos_2nd'
    
    video_files = {f.split('.')[0]: os.path.join(video_dir, f) 
                   for f in os.listdir(video_dir) if f.endswith('.mp4')}
    srt_files = {f.split('.')[0]: os.path.join(srt_dir, f) 
                 for f in os.listdir(srt_dir) if f.endswith('.srt')}
    
    for video_id in tqdm(video_files.keys(), desc='Processing videos'):
        if video_id in srt_files:
            times = parse_srt(srt_files[video_id])
            slice_video(video_files[video_id], times, output_dir, video_id, max_workers=8)

if __name__ == '__main__':
    main()