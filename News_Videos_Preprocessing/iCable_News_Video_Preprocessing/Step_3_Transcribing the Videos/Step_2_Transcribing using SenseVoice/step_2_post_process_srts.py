import os
import pandas as pd
from tqdm import tqdm
import emoji
import re
import opencc
import pycantonese
import multiprocessing

folder_path = r"./icable_SRT_Transcribing/srts_sensevoice/srts"
output_path = r"./icable_SRT_Transcribing/srts_sensevoice/combined_transcripts_final.csv"

data = []
for filename in tqdm(os.listdir(folder_path)):
    if filename.endswith('.txt'):
        video_id = filename[:-4]
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            transcript = file.read().strip()
        data.append({'video_id': video_id, 'transcript': transcript})

df = pd.DataFrame(data)

chinese_punctuations = "，。！？、；：（）【】《》「」『』……—～﹁﹂﹃﹄"
punctuation_pattern = "[" + re.escape(chinese_punctuations) + "]"

def remove_emoji_and_punctuation(text):
    text_no_emoji = emoji.replace_emoji(text, replace="")
    text_clean = re.sub(punctuation_pattern, "", text_no_emoji)
    return text_clean

df["transcript"] = df["transcript"].apply(remove_emoji_and_punctuation)

converter = opencc.OpenCC('s2t.json')

def convert_to_trad(text):
    result = ''
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            result += converter.convert(char)
        else:
            result += char
    return result

tqdm.pandas()
df['transcript_trad'] = df['transcript'].apply(convert_to_trad)

def convert_to_jyutping(text):
    result = pycantonese.characters_to_jyutping(text)
    jyutping_list = []
    for word, jp in result:
        if jp is None:
            if re.fullmatch(r'[A-Za-z]+', word):
                for char in word.upper():
                    jyutping_list.append(char)
                continue
            else:
                return None
        split_jp = re.findall(r'[a-z]+\d', jp)
        if len(split_jp) == len(word):
            jyutping_list.extend(split_jp)
        else:
            return None
    return ' '.join(jyutping_list)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    df['jyutping'] = df['transcript_trad'].progress_apply(convert_to_jyutping)

def remove_tone_numbers(jyutping_str):
    if pd.isna(jyutping_str):
        return jyutping_str
    syllables = jyutping_str.split()
    processed_syllables = [syllable[:-1] if syllable[-1].isdigit() else syllable for syllable in syllables]
    return ' '.join(processed_syllables)

df['jyutping'] = df['jyutping'].apply(remove_tone_numbers)
df.dropna(subset=['jyutping'], inplace=True)
df.to_csv(output_path, index=False, encoding='utf-8')

print(f"Processed file saved as: {output_path}")