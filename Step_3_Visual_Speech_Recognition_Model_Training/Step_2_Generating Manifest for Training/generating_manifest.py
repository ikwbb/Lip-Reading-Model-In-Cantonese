import pandas as pd
import cv2
import os
from tqdm import tqdm
from auto_avsr.preparation.transforms import TextTransform

text_transform = TextTransform()

def transcript_to_token(transcript):
    token_ids = text_transform.tokenize(transcript)
    if token_ids is None or len(token_ids) == 0:
        print(f"Warning: No tokens generated for transcript: {transcript}")
        return ''
    token_id_str = " ".join(map(str, token_ids.tolist()))
    return token_id_str

transcript_csv_path = './combined_transcripts_final.csv' # This file is generated in Preprocessing Step 3: Transcribing the Videos
video_dir = "../../datasets/tvb_dataset/cstm/cstm_video_seg24s"
# video_dir = "./auto_avsr_dataset_tvb/cstm/cstm_video_seg24s"
output_csv_path = './training_dataset_tvb.csv' # or ./training_dataset_icable.csv

# Step 1: Read and tokenize transcripts
df_transcripts = pd.read_csv(transcript_csv_path)
df_transcripts['token'] = df_transcripts['jyutping'].apply(transcript_to_token)
print(f"Number of transcripts: {len(df_transcripts)}")

# Step 2: Process video files
mp4_files = [f for f in os.listdir(video_dir) if f.endswith('.mp4')]
video_data = []
for mp4_file in tqdm(mp4_files, desc="Processing videos"):
    video_path = os.path.join(video_dir, mp4_file)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {mp4_file}")
        continue
    input_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_id = mp4_file.replace('.mp4', '')
    video_data.append({'video_id': video_id, 'input_length': input_length})
    cap.release()
df_videos = pd.DataFrame(video_data)
print(f"Number of videos processed: {len(df_videos)}")

# Step 3: Merge transcripts with video data
merged_df = pd.merge(df_transcripts, df_videos, on='video_id', how='inner')
print(f"Number of merged rows: {len(merged_df)}")

# Step 4: Construct the training dataset
final_df = pd.DataFrame()
final_df['cstm'] = 'cstm'
final_df['path'] = 'cstm_video_seg24s/' + merged_df['video_id'] + '.mp4'
final_df['input_length'] = merged_df['input_length']
final_df['token'] = merged_df['token']

# Step 5: Filter based on input_length < 700
final_df = final_df[final_df['input_length'] < 700]
print(f"Number of rows after filtering: {len(final_df)}")

# Save the final result
final_df.to_csv(output_csv_path, index=False)
print(f"Processing completed, saved to {output_csv_path}")