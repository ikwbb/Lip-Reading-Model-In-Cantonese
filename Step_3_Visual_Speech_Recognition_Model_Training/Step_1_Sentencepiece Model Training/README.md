# SentencePiece Encoding and Training

This folder contains scripts for training a SentencePiece model and encoding text using the trained model. The provided tools are built to preprocess text data for natural language processing tasks, such as tokenization and vocabulary generation.

## Overview

The project includes three main scripts:
- **`spm_train.py`**: Trains a SentencePiece model on input text data.
- **`spm_encode.py`**: Encodes text using a trained SentencePiece model, with options to filter by token length and output format (piece or ID).
- **`train.sh`**: A shell script that automates the process of training a SentencePiece model and generating a dictionary file.

These scripts leverage the [SentencePiece](https://github.com/google/sentencepiece) library for subword tokenization.

## Prerequisites

To use these scripts, you need the following:
- Python 3.6+
- [SentencePiece](https://github.com/google/sentencepiece) Python library (`pip install sentencepiece`)
- Bash shell (for running `train.sh`)



## Example Workflow

1. Prepare an input text file (`input.txt`) with your training data. This file can be obtained by extracting the `jyutping` column in the `combined_transcripts_final.csv` from Preprocessing Step 3.

2. Run the training script:
   ```bash
   bash train.sh
   ```

3. In **Step_4_VSR Model Training**, replace the folder `auto_avsr/spm/unigram` by using the generated Sentencepiece model under `./unigram`.

4. In **Step_4_VSR Model Training**, replace the model name from `unigram5000.model` to `unigram1090.model` in `auto_avsr/preparation/transforms.py` and `auto_avsr/datamodule/transforms.py`.



## Detailed Usage

### 1. Training a SentencePiece Model (`spm_train.py`)

This script trains a SentencePiece model on your input text data.

**Command:**

```bash
python spm_train.py --input=<input_file> --model_prefix=<model_name> --vocab_size=<vocab_size> --model_type=<model_type>
```

**Example:**

```bash
python spm_train.py --input=input.txt --model_prefix=unigram_model --vocab_size=1000 --model_type=unigram
```

**Arguments:**

- `--input`: Path to the input text file.
- `--model_prefix`: Prefix for the output model and vocabulary files.
- `--vocab_size`: Size of the vocabulary.
- `--model_type`: Model type (e.g., `unigram`, `bpe`).

### 2. Encoding Text (`spm_encode.py`)

This script encodes text using a trained SentencePiece model.

**Command:**

```bash
python spm_encode.py --model=<model_file> --inputs=<input_file> --outputs=<output_file> --output_format=<format> [--min-len=<N>] [--max-len=<N>]
```

**Example:**

```bash
python spm_encode.py --model=unigram_model.model --inputs=input.txt --outputs=encoded.txt --output_format=piece --min-len=2 --max-len=50
```

**Arguments:**

- `--model`: Path to the trained SentencePiece model file (`.model`).
- `--inputs`: Input file(s) to encode (use `-` for stdin).
- `--outputs`: Output file(s) for encoded text (use `-` for stdout).
- `--output_format`: Output format (`piece` for subword pieces, `id` for token IDs).
- `--min-len`: Optional minimum token length filter.
- `--max-len`: Optional maximum token length filter.

### 3. Automating Training and Dictionary Generation (`train.sh`)

The `train.sh` script automates the process of training a SentencePiece model and creating a dictionary file.

**Command:**

```bash
bash train.sh
```

**What it does:**

- Sets up a directory for the model (`unigram` by default).
- Trains a SentencePiece model with a vocabulary size of 1090 (configurable via `nbpe`).
- Generates a dictionary file (`unigram/unigram1090_units.txt`) with subword units and their indices.
- Includes `<unk>` as a special token with ID 1.

**Customization:**

- Modify `nbpe` to change the vocabulary size.
- Update `bpemode` to use a different model type (e.g., `bpe`).
- Ensure `input.txt` exists in the working directory.

**Example output files:**

- `unigram/unigram1090.model`: Trained SentencePiece model.
- `unigram/unigram1090.vocab`: Vocabulary file.
- `unigram/unigram1090_units.txt`: Dictionary file with subword units.



## Notes

- The scripts assume UTF-8 encoded input files.
- `<unk>` is reserved as token ID 1 in the dictionary, and ID 0 is reserved for the CTC "blank" token.
- The `train.sh` script processes up to 100,000,000 sentences by default (configurable in `spm_train.py` arguments).
- For large datasets, monitor memory usage during training.
