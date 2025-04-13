import json
import pandas as pd
import pycantonese
import re
from tqdm import tqdm
import multiprocessing

def convert_to_jyutping(text):
    """Convert Cantonese text to Jyutping."""
    result = pycantonese.characters_to_jyutping(text)
    jyutping_list = []

    for word, jp in result:
        if jp is None:
            if re.fullmatch(r'[A-Za-z]+', word):
                for char in word.upper():
                    jyutping_list.append(char)
                continue
            else:
                print(f"Encountered error in text: {text}")
                return None

        split_jp = re.findall(r'[a-z]+\d', jp)
        if len(split_jp) == len(word):
            jyutping_list.extend(split_jp)
        else:
            print(f"Cannot match jyutping length for word: {word}, jp: {jp}")
            return None
    
    return ' '.join(jyutping_list)

def remove_tone_numbers(jyutping_str):
    """Remove tone numbers from Jyutping string."""
    if pd.isna(jyutping_str):
        return jyutping_str
    syllables = jyutping_str.split()
    processed_syllables = [syllable[:-1] if syllable[-1].isdigit() else syllable for syllable in syllables]
    return ' '.join(processed_syllables)

def process_json_to_dataframe(json_file_path):
    """Process JSON file to DataFrame with Jyutping conversion."""
    yue_list = []
    zh_list = []
    
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        for line in json_file:
            data = json.loads(line)
            yue = data['translation']['yue']
            zh = data['translation']['zh']
            yue_list.append(yue)
            zh_list.append(zh)
    
    df = pd.DataFrame({'yue': yue_list, 'zh': zh_list})
    
    tqdm.pandas()
    df['jyutping'] = df['yue'].progress_apply(convert_to_jyutping)
    df.dropna(subset=['jyutping'], inplace=True)
    df['jyutping'] = df['jyutping'].apply(remove_tone_numbers)
    
    return df

def main():
    json_file_path = r"./train.json"
    output_file_path = r"./train_jyutping_no_tone.csv"
    
    multiprocessing.freeze_support()
    df = process_json_to_dataframe(json_file_path)
    df.to_csv(output_file_path, index=False, encoding='utf-8')
    print(f"Processed file saved as: {output_file_path}")

if __name__ == '__main__':
    main()