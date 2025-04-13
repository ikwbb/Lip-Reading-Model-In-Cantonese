# Checkpoint to PyTorch Model Converter

This script converts a model checkpoint file to a PyTorch model state dictionary file.



## Prerequisites

- Python 3.x
- PyTorch (`torch` library)

Install the required dependency:
```bash
pip install torch
```



## Usage

The script accepts two command-line arguments:
- `--checkpoint`: Path to the input checkpoint file (required)
- `--output`: Path to save the output PyTorch model file (required)

### Example

```bash
python script.py --checkpoint /path/to/epoch_20.ckpt --output /path/to/model_20.pth
```

After generating the pth file, copy the trained models to the directories`icable_models`, `tvb_models`, or `mixed_models`, which specify the path to the model, indicating the dataset it was trained on. (For example, if the model was trained on the TVB dataset, use `tvb`.)

### Help

To display usage information:
```bash
python script.py --help
```



## Script Description

The script performs the following steps:
1. Loads the checkpoint file using `torch.load`.
2. Extracts the model state dictionary, removing the `model.` prefix from keys.
3. Saves the processed state dictionary to the specified output path as a `.pth` file.
