import os
from model import SenseVoiceSmall
from funasr.utils.postprocess_utils import rich_transcription_postprocess
from tqdm import tqdm


model_dir = "iic/SenseVoiceSmall"
m, kwargs = SenseVoiceSmall.from_pretrained(model=model_dir, device="cuda:0")
m.eval()

# Path to the Audio Files
audio_dir = r"./TVB_Trim/trimmed_audios"

# Output Path to the SRT Transcription Files
output_dir = r"./TVB_SRT_Transcribing/srts_sensevoice/srts"


audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.m4a')]
existing_files = set(f for f in os.listdir(output_dir) if f.endswith('.txt'))
audio_files_to_process = [
    f for f in audio_files if os.path.splitext(f)[0] + '.txt' not in existing_files
]


for audio_file in tqdm(audio_files_to_process, desc="Processing audio files"):
    
    audio_path = os.path.join(audio_dir, audio_file)
    print(f"Processing {audio_file}...")
    res = m.inference(
        data_in=audio_path,
        language="yue",  
        use_itn=True,    
        ban_emo_unk=True,  
        **kwargs,
    )
    text = rich_transcription_postprocess(res[0][0]["text"])
    text = text.replace('\n', ' ')
    output_file = os.path.splitext(audio_file)[0] + '.txt'
    output_path = os.path.join(output_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Saved to {output_path}")