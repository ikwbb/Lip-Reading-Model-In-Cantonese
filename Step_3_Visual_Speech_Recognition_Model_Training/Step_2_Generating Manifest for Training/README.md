# Auto AVSR Dataset Preparation

This project contains a Python script for preparing a training dataset for Automatic Video Speech Recognition (AVSR) by combining video files with their corresponding tokenized transcripts. The script processes MP4 video files, tokenizes transcripts using a custom `TextTransform` class, merges the data, and generates a final CSV file suitable for training.



## Overview

The script performs the following tasks:
1. Reads and tokenizes transcripts from a CSV file using the `TextTransform` class.
2. Processes MP4 video files to extract metadata (e.g., frame count).
3. Merges transcript and video data based on video IDs.
4. Constructs a training dataset with video paths, input lengths, and tokenized transcripts.
5. Filters out videos with an input length greater than or equal to 700 frames.
6. Saves the resulting dataset to a CSV file.



## Prerequisites

- Python 3.8 or higher
- Required Python packages:
  - `pandas`
  - `opencv-python` (cv2)
  - `tqdm`
- A custom `TextTransform` class (assumed to be available in the `auto_avsr.preparation.transforms` module).
- Input files:
  - A CSV file containing transcript data (`combined_transcripts_final.csv` from Preprocessing Step 3).
  - A directory containing MP4 video files (`../../datasets/tvb_dataset/cstm/cstm_video_seg24s`).



## Usage

1. Update the script with the correct paths to your input files and output directory:
   - `transcript_csv_path`: Path to the transcript CSV file.
   - `video_dir`: Directory containing MP4 video files.
   - `output_csv_path`: Path where the final dataset CSV will be saved.

2. Run the script:
   ```bash
   python prepare_dataset.py
   ```

3. The script will process the data and save the output to the specified `output_csv_path`.



## Script Details

The script (`prepare_dataset.py`) performs the following steps:

1. **Read and Tokenize Transcripts**:
   - Loads the transcript CSV file using `pandas`.
   - Applies the `transcript_to_token` function to convert `jyutping` transcripts into tokenized strings using the `TextTransform` class.

2. **Process Video Files**:
   - Iterates through MP4 files in the specified directory.
   - Uses OpenCV (`cv2`) to extract the frame count (`input_length`) for each video.
   - Stores video metadata in a DataFrame.

3. **Merge Data**:
   - Merges transcript and video DataFrames on the `video_id` column using an inner join.

4. **Construct Training Dataset**:
   - Creates a new DataFrame with columns: `cstm`, `path`, `input_length`, and `token`.
   - Constructs relative video paths for compatibility (e.g., `cstm_video_seg24s/<video_id>.mp4`).

5. **Filter and Save**:
   - Filters out rows where `input_length` is 700 or greater.
   - Saves the final dataset to a CSV file.



## Input and Output

### Input
- **Transcript CSV** (`combined_transcripts_final.csv`):
  - Expected columns: `video_id`, `jyutping` (other columns are ignored).
  - Contains transcript data for each video, where `jyutping` is tokenized.
- **Video Directory** (`../../datasets/tvb_dataset/cstm/cstm_video_seg24s`):
  - Contains MP4 video files named `<video_id>.mp4`.

### Output
- **Training Dataset CSV** (`training_dataset_tvb.csv`):
  - Columns:
    - `cstm`: Constant value (`cstm`).
    - `path`: Relative path to the video file (e.g., `cstm_video_seg24s/<video_id>.mp4`).
    - `input_length`: Number of frames in the video.
    - `token`: Space-separated string of token IDs for the transcript.
  - Only includes videos with `input_length < 700`.