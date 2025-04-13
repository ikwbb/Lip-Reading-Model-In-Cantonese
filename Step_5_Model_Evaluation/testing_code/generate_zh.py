import os
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import pandas as pd
from tqdm import tqdm
import argparse


# =========== Ambiguous Jyutping Mapping (Deprecated) ===========
initials = ['gw', 'kw', 'ng', 'b', 'p', 'm', 'f', 'd', 't', 'n', 'l', 'g', 'k', 'h', 'z', 'c', 's', 'j', 'w']

def get_initial_final(syllable):
    for init in initials:
        if syllable.startswith(init):
            return init, syllable[len(init):]
    return '', syllable

def replace_syllable(syllable):
    init, final = get_initial_final(syllable)
    if init in ['b', 'p', 'm']:
        new_init = 'b'
    elif init in ['d', 't', 'z', 'c', 's', 'j', 'n', 'ng', 'g', 'k']:
        new_init = 'd'
    elif init in ['gw', 'kw', 'w']:
        new_init = 'w'
    else:
        new_init = init
    return new_init + final

def replace_jyutping(jyutping):
    if pd.isna(jyutping):
        return ''
    syllables = jyutping.split()
    new_syllables = [replace_syllable(syl) for syl in syllables]
    return ' '.join(new_syllables)
# =============================================================

# Parse command line arguments
parser = argparse.ArgumentParser(description="Using specified LoRA Adapter to generate Cantonese translation from Jyutping")
parser.add_argument("--lora", type=str, required=True, default="absolute", choices=["absolute", "ambiguous"],
                    help="Choices of LoRA Adapter'absolute' or 'ambiguous'")
parser.add_argument("--input_csv", type=str, required=True,
                    help="Path to the input CSV file")
parser.add_argument("--output_csv", type=str, required=True,
                    help="Path to the output CSV file")
args = parser.parse_args()

# Set LoRA Adapter path based on --lora argument
if args.lora == "absolute":
    lora_model_path = "../../lora-checkpoints/cantonese-lora-checkpoint-absolute"
elif args.lora == "ambiguous":
    lora_model_path = "../../lora-checkpoints/cantonese-lora-checkpoint-ambiguous"

# Loading tokenizer and base model
base_model_name = "hon9kon9ize/CantoneseLLMChat-v1.0-7B"
tokenizer = AutoTokenizer.from_pretrained(base_model_name, use_fast=False)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    device_map="cuda",
    torch_dtype=torch.bfloat16
).eval()


lora_model = PeftModel.from_pretrained(base_model, lora_model_path)
lora_model.generation_config.pad_token_id = tokenizer.pad_token_id


def generate_cantonese(jyutping_input):
    system_message = "你是一個粵語翻譯助手。你的任務是將粵拼（Jyutping）翻譯成對應的廣東話文字。"
    user_prompt = f"請將以下粵拼翻譯成廣東話：\n{jyutping_input}"
    prompt_text = (
        f"<|im_start|>system\n{system_message}<|im_end|>\n"
        f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
        f"<|im_start|>assistant\n"
    )
    inputs = tokenizer(prompt_text, return_tensors="pt").to("cuda")
    with torch.no_grad():
        outputs = lora_model.generate(
            **inputs,
            max_new_tokens=100,
            temperature=0.1,
            do_sample=True
        )
    generated_ids = outputs[0][inputs.input_ids.shape[1]:]
    decoded_output = tokenizer.decode(generated_ids, skip_special_tokens=True)
    return decoded_output.strip()


df = pd.read_csv(args.input_csv)
predicted_cantonese = []

for index, row in tqdm(df.iterrows(), total=len(df), desc="Generating Cantonese"):
    # Convert Jyutping to ambiguous form if ambiguous LoRA adapter is used
    if args.lora == "ambiguous":
        prediction_input = replace_jyutping(row['prediction'])
    else:
        prediction_input = row['prediction']
    
    predicted_cantonese.append(generate_cantonese(prediction_input))

df['predicted_cantonese'] = predicted_cantonese
df.to_csv(args.output_csv, index=False)