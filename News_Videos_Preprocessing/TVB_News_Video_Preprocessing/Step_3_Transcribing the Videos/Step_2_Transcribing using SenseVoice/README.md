# Audio Transcription with SenseVoice-Small

This script transcribes audio files (.m4a) using the `SenseVoiceSmall` model and saves the transcriptions as text files (.txt).

## Requirements

- Python 3.x
- Required packages:
  - `torch` (with CUDA support for GPU)
  - `funasr`
  - `tqdm`
- Pre-trained model: `SenseVoiceSmall` (downloaded to `iic/SenseVoiceSmall`)

Install dependencies:
```bash
pip install torch funasr tqdm# Audio Transcription with SenseVoiceSmall
```

This script transcribes audio files (.m4a) using the `SenseVoiceSmall` model and saves the transcriptions as text files (.txt).



## Execution

1. Locate the `step_1_get_transcription.py` and edit the path to the **audio files** and the **output SRT files**.

```python
# Path to the Audio Files
audio_dir = r"./TVB_Trim/trimmed_audios"

# Output Path to the SRT Transcription Files
output_dir = r"./TVB_SRT_Transcribing/srts_sensevoice/srts"
```

3. Execute `./step_1_get_transcription.py` to generate the Audio Transcription.
4. Locate the `post_process_srts.py` and edit the path to the **audio files** and the **output SRT files**.

```python
folder_path = r"./TVB_SRT_Transcribing/srts_sensevoice/srts"
output_path = r"./TVB_SRT_Transcribing/srts_sensevoice/combined_transcripts_final.csv"
```

5. Execute `./post_process_srts.py` to post process the generated transcription.