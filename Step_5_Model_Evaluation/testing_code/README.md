# Cantonese Lip-Reading Evaluation

This project provides a pipeline to evaluate Automatic Video Speech Recognition (AVSR) models, translate Jyutping predictions to Cantonese text using a fine-tuned language model, and generate a comprehensive manifest with ground truth and predicted data.



## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Directory Structure](#directory-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Scripts](#scripts)
- [Output](#output)
- [Notes](#notes)



## Overview

The pipeline performs the following tasks:
1. Evaluates an AVSR model on a specified dataset using `eval.py` (invoked via `start_eval.sh`).
2. Translates Jyutping predictions to Cantonese text using a LoRA-adapted language model (`generate_zh.py`).
3. Merges predictions, ground truth, and metadata into a final manifest (`generate_full_manifest.py`).



## Prerequisites

- **Python 3.8+**
- **Bash** (for running `start_eval.sh`)
- **Dependencies**:
  - `transformers`
  - `peft`
  - `torch`
  - `pandas`
  - `tqdm`
- **Hardware**: GPU with CUDA support (recommended for `generate_zh.py`).
- **Model Checkpoints**:
  - Pretrained AVSR model (specified in `start_eval.sh`).
  - LoRA checkpoints for Cantonese translation (e.g., `cantonese-lora-checkpoint-absolute` or `cantonese-lora-checkpoint-ambiguous`).
- **Dataset**: A video dataset (e.g., TVB or iCable) with corresponding labels and ground truth CSV files.

Install Python dependencies:
```bash
pip install transformers peft torch pandas tqdm
```



## Setup

1. **Clone the Repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Prepare Datasets**:
   - Place dataset files in `datasets/{dataset}_dataset/` with a `labels/cstm_test.csv` file.
   - Ensure ground truth files (`tvb_gt.csv`, `icable_gt.csv`) are in `datasets/ground_truth_labels/`.

3. **Download Models**:
   - Place the pretrained AVSR model in a directory accessible to `start_eval.sh`.
   - Download the base Cantonese LLM (`hon9kon9ize/CantoneseLLMChat-v1.0-7B`) and LoRA checkpoints in `lora-checkpoints/`.

4. **Set Permissions**:
   ```bash
   chmod +x start_eval.sh
   ```



## Usage

Run the pipeline using `start_eval.sh` with required arguments:
```bash
./start_eval.sh --dataset <dataset> --epoch <epoch> --lora <lora> --model <model> [--check] [--shutdown]
```



### Arguments

- `--dataset`: Dataset name (e.g., `tvb`, `icable`).
- `--epoch`: Epoch number of the pretrained AVSR model.
- `--lora`: LoRA adapter for Cantonese translation (`absolute` or `ambiguous`).
- `--model`: Specify the path to the model, indicating the dataset it was trained on. For example, if the model was trained on the TVB dataset, use `tvb`. (`tvb`, `icable` or `mixed`)
- `--check`: Flag to check the evaluation on 20 samples.
- `--shutdown`: If specified, shuts down the system after completion (with a 60-second delay).



### Example

```bash
./start_eval.sh --dataset icable --epoch 76 --lora absolute --model icable --check
```

This command:
1. Evaluates the AVSR model on the `tvb` dataset.
2. Translates Jyutping predictions to Cantonese using the `absolute` LoRA adapter.
3. Generates a full manifest with ground truth and predictions.
4. Shuts down the system after completion.



## Scripts

### `start_eval.sh`
- **Purpose**: Orchestrates the evaluation pipeline.
- **Steps**:
  1. Runs `eval.py` to generate AVSR predictions (skipped if output CSV exists).
  2. Calls `generate_zh.py` to translate predictions to Cantonese (skipped if output CSV exists).
  3. Calls `generate_full_manifest.py` to create a merged manifest (skipped if output CSV exists).
  4. Optionally shuts down the system if `--shutdown` is specified.
- **Outputs**: CSVs in `testing_results/` and a log file.

### `generate_zh.py`
- **Purpose**: Translates Jyutping predictions to Cantonese text.
- **Features**:
  - Uses a LoRA-adapted `CantoneseLLMChat-v1.0-7B` model.
  - Supports `absolute` (direct translation) or `ambiguous` (maps certain initials for flexibility) LoRA adapters.
  - Processes input CSV and appends a `predicted_cantonese` column.
- **Input**: CSV with a `prediction` column (Jyutping).
- **Output**: CSV with predicted Cantonese text.

### `generate_full_manifest.py`
- **Purpose**: Merges AVSR predictions, Cantonese translations, and ground truth data.
- **Features**:
  - Combines data based on `video_id`.
  - Supports `tvb` or `icable` ground truth datasets.
  - Outputs a CSV with columns: `index`, `prediction`, `ground_truth`, `transcript_trad`, `predicted_cantonese`, `video_id`, `tokens`, `video_path`.
- **Input**: AVSR prediction CSV, Cantonese translation CSV, index CSV, ground truth CSV.
- **Output**: Merged CSV in `testing_results/full/`.



## Output

Results are saved in `testing_results/`:
- `result_{dataset}_{epoch}_epoch_test.csv`: AVSR evaluation results.
- `zh/result_{dataset}_{epoch}_epoch_test_{lora}_zh.csv`: Cantonese translations.
- `full/result_{dataset}_{epoch}_epoch_test_{lora}_full.csv`: Final manifest with all data.
- `result_{dataset}_{epoch}_epoch_test_{lora}.txt`: Log file from `eval.py`.



## Notes

- Ensure sufficient disk space for model checkpoints and output CSVs.
- The `eval.py` script is assumed to exist in `auto_avsr/` (not provided here).
- The `ambiguous` LoRA adapter in `generate_zh.py` uses a deprecated syllable mapping; consider using `absolute` for better accuracy.
- If a CSV already exists, the corresponding script is skipped to avoid overwriting.
- Use `--shutdown` cautiously, as it triggers a system shutdown with a 60-second delay.
