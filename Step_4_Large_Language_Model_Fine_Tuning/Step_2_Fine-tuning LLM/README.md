# Cantonese Jyutping to Text Translator

This Jupyter Notebook `fine_tuning_llm_for_jyutping_to_cantonese_conversion.ipynb` fine-tunes a large language model to translate Jyutping (a romanization system for Cantonese) into corresponding Cantonese text using LoRA (Low-Rank Adaptation) with the `hon9kon9ize/CantoneseLLMChat-v1.0-7B` model.



## Overview
The script performs the following tasks:
1. Loads a pre-trained Cantonese language model and tokenizer.
2. Processes a dataset (`train_jyutping_no_tone.csv`) containing Jyutping and corresponding Cantonese text.
3. Fine-tunes the model using LoRA to translate Jyutping to Cantonese text.
4. Saves the fine-tuned model for inference.
5. Provides a function to generate Cantonese text from Jyutping input using the fine-tuned model.



## Requirements

To run this project, install the required Python packages:

```bash
pip install transformers peft torch pandas datasets
```

Additional requirements:
- A CUDA-enabled GPU for faster training and inference (optional but recommended).
- The dataset file `train_jyutping_no_tone.csv`.



## Dataset

The dataset (`train_jyutping_no_tone.csv`) should have the following structure:

| yue                          | jyutping (without tone)                     |
|------------------------------|-----------------------------------------------|
| 泥水佬開門口過得人過得自己 | nai seoi lou hoi mun hau gwo dak jan gwo dak zi gei |
| 杞人嘅朋友嘆咗一口氣       | gei jan ge pang jau taan zo jat hau hei |

- `yue`: Cantonese text.
- `jyutping`: Corresponding Jyutping romanization (without tone markers).



## Setup

1. **Environment Configuration**: If AutoDL is used, uncomment and configure the environment variables for Hugging Face:
   
   ```python
   os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
   ```

2. **Model and Tokenizer**: The script uses the `hon9kon9ize/CantoneseLLMChat-v1.0-7B` model. Ensure an internet connection to download the model or configure a local cache.

3. **Dataset**: Place the `train_jyutping_no_tone.csv` file in the working directory.



## Training

The script fine-tunes the model using LoRA with the following steps:
1. **Data Preparation**:
   - Loads the CSV dataset.
   - Formats examples into prompts with a system message and user input.
   - Tokenizes the dataset for training.

2. **LoRA Configuration**:
   - Targets specific model modules (`q_proj`, `k_proj`, `v_proj`, etc.).
   - Uses rank `r=8`, `lora_alpha=32`, and `lora_dropout=0.05`.

3. **Training Arguments**:
   - Output directory: `./cantonese-llm-lora-output`.
   - Batch size: 8 (with gradient accumulation).
   - Epochs: 3.
   - Learning rate: 1e-4.
   - Uses `bf16` precision for efficiency.

4. **Running Training**:
   Execute the script to start training:
   ```bash
   python script.py
   ```
   The fine-tuned model is saved to `cantonese-lora-checkpoint`.



## Inference

The script includes a function to generate Cantonese text from Jyutping input using the fine-tuned model.

1. **Loading the Model**:
   - Loads the base model and applies the LoRA weights from `cantonese-lora-checkpoint`.

2. **Generating Output**:
   - Takes a Jyutping string as input.
   - Constructs a prompt and generates the corresponding Cantonese text.

Example usage:
```python
test_input = "m hai gong siu zan hai gei sai lei"
prediction = generate_cantonese(test_input)
print("Prediction:", prediction)
```



## Usage

To use the script:
1. Ensure all dependencies are installed.
2. Prepare the dataset (`train_jyutping_no_tone.csv`).
3. Run the script to train the model:
   ```bash
   python script.py
   ```
4. Use the `generate_cantonese` function for inference:
   ```python
   prediction = generate_cantonese("m hai gong siu zan hai gei sai lei")
   print(prediction)  # Expected output: 唔係講笑真係幾犀利
   ```
