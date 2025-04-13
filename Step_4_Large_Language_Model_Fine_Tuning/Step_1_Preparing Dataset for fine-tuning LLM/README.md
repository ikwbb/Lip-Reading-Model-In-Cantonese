# Script to create fine-tuning dataset for LLM

This Python script processes a JSON file containing Cantonese (yue) and Mandarin (zh) translations, converts the Cantonese text to Jyutping (Cantonese romanization), removes tone numbers, and saves the result to a single CSV file. The script combines JSON parsing, Jyutping conversion, and tone number removal into one efficient process without creating intermediate files. The generated CSV file will be used for fine-tuning Large Language Model (LLM).



## Features

- Reads JSON input containing Cantonese and Mandarin translations
- Converts Cantonese text to Jyutping using `pycantonese`
- Removes tone numbers from Jyutping output
- Saves results to a CSV file with columns: `yue`, `zh`, and `jyutping`
- Includes progress tracking with `tqdm`
- Handles special cases (e.g., English words in text)
- Uses multiprocessing for efficiency



## Prerequisites

- Python 3.6 or higher
- Required Python packages:
  ```bash
  pip install pandas pycantonese tqdm
  ```
  



## Input Data

The script expects a JSON file (`train.json`) with Cantonese and Mandarin translations. You can download suitable datasets from the following sources:
- [Cantonese-Traditional Chinese Parallel Corpus](https://huggingface.co/datasets/raptorkwok/cantonese-traditional-chinese-parallel-corpus)
- [Cantonese-Mandarin Translations](https://huggingface.co/datasets/botisan-ai/cantonese-mandarin-translations)

Combine and place the downloaded JSON files in a`train.json` file in the directory: `./`.



## Usage

1. Ensure the `train.json` file is in the correct directory (`./`).
2. Install the required Python packages (see Prerequisites).
3. Run the script:
   ```bash
   python create_training_set_for_fine_tuning_LLM.py
   ```
4. The output will be saved as `train_jyutping_no_tone.csv` in the same directory.

## Output
The output CSV file (`train_jyutping_no_tone.csv`) contains three columns:
- `yue`: Original Cantonese text
- `zh`: Mandarin translation
- `jyutping`: Jyutping romanization of the Cantonese text (without tone numbers)

## Notes
- The script assumes sufficient memory to process the entire dataset. For very large datasets, consider modifying the script to process data in chunks.
- Error handling is included for cases where Jyutping conversion fails (e.g., unsupported characters or mismatched lengths).
- English words in the Cantonese text are converted to uppercase letters in the Jyutping output.

## Directory Structure
Ensure your directory structure looks like this:
```
./
├── train.json
├── create_training_set_for_fine_tuning_LLM.py
└── train_jyutping_no_tone.csv (generated after running the script)
```
