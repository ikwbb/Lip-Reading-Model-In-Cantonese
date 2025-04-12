# News Video Thumbnail Analysis and Classification

## Overview
This Jupyter Notebook processes a collection of news video clips to generate thumbnails, extract visual features, manually label thumbnails, and classify them based on whether they contain news reporters. The pipeline includes:

1. **Thumbnail Generation**: Extract the first frame from each video clip and save it as a thumbnail image.
2. **Feature Extraction**: Use OpenAI's CLIP pretrained model to extract features from the thumbnails.
3. **Manual Labeling**: Provide a GUI tool to manually label thumbnails as "Having News Reporters" or "Does NOT Have News Reporters."
4. **Classification**: Train a neural network to classify thumbnails based on the presence of news reporters and predict labels for unlabeled data.

The goal is to automate the classification of news video thumbnails to identify those featuring reporters, using a combination of computer vision and machine learning techniques.

## Prerequisites
To run this notebook, you need the following dependencies installed:

- Python 3.8+
- Jupyter Notebook or JupyterLab
- Libraries:
  ```bash
  pip install opencv-python torch torchvision torchaudio clip pandas numpy pillow tqdm scikit-learn tkinter
  ```

Additionally, ensure you have:
- A folder containing `.mp4` video files (default: `./iCable Scraped Videos`).
- Access to a GPU (optional but recommended for faster CLIP feature extraction).

## Directory Structure
The notebook assumes the following folder structure:
```
project_directory/
│
├── iCable Scraped Videos/           # Input folder with .mp4 video files
├── thumbnails/                   # Output folder for generated thumbnails
├── iCable_clip_features.pkl         # Saved CLIP features
├── iCable_labels.csv               # Manual labels
├── complex_classifier.pth        # Trained neural network model
├── labels_predicted.csv         # Final predicted labels
└── iCable_News_Scene_Classifyer.ipynb                # The Jupyter Notebook
```

## Usage
1. Open the Jupyter Notebook:
   ```bash
   jupyter notebook iCable_News_Scene_Classifyer.ipynb
   ```
2. Run the cells sequentially. The notebook is divided into four main sections (described below).
3. For the manual labeling section, use the GUI to label images as `True` (has reporters) or `False` (no reporters). Keyboard shortcuts are available: `j` for True, `k` for False, and `h` to go back.

### Notebook Sections
1. **Generating Thumbnails for Each News Video Clip**:
   - Extracts the first frame from each `.mp4` video in the input folder.
   - Saves thumbnails as `.jpg` files in the `thumbnails` folder.
   - Uses multithreading for faster processing with `ThreadPoolExecutor`.

2. **Generating Features for the First Frame Using CLIP**:
   - Loads OpenAI's CLIP model (`ViT-L/14@336px`) to extract 768-dimensional feature vectors from thumbnails.
   - Saves the features as a pandas DataFrame in `iCable_clip_features.pkl`.

3. **Manually Labeling Thumbnails**:
   - Provides a Tkinter-based GUI to label thumbnails as "Having News Reporters" or "Does NOT Have News Reporters."
   - Labels are saved incrementally to `iCable_labels.csv`.
   - Supports resuming labeling from where you left off.

4. **Classifying Videos Using a Neural Network**:
   - Trains a simple feedforward neural network to classify thumbnails based on CLIP features.
   - Evaluates the model using a test set and prints a classification report.
   - Saves the trained model as `complex_classifier.pth`.
   - Predicts labels for unlabeled thumbnails and saves the results to `labels_predicted.csv`.

## Output Files
- `thumbnails/`: Contains `.jpg` thumbnail images.
- `iCable_clip_features.pkl`: CLIP feature vectors for all thumbnails.
- `iCable_labels.csv`: Manually assigned labels for thumbnails.
- `complex_classifier.pth`: Trained neural network weights.
- `labels_predicted.csv`: Final predictions for all thumbnails (labeled and unlabeled).
