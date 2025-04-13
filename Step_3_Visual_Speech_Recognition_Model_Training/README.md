# VSR Model Training Pipeline

This README outlines the steps to train the Visual Speech Recognition (VSR) model.



## Step 1: Train Sentencepiece Model

Convert Jyutping to tokens by training a sentencepiece model. Follow the instructions in `Step_1_Sentencepiece_Model_Training/README.md`.



## Step 2: Generate Manifest

Prepare a manifest file for VSR model training. See `Step_2_Generating_Manifest_for_Training/README.md` for details.



## Step 3: Split Dataset

Split the dataset into training (80%), validation (10%), and test (10%) sets:
1. Use the `training_dataset_icable.csv` file in `Step_3_Splitting_Dataset/iCable` or `Step_3_Splitting_Dataset/TVB`.
2. Run `step_1_split_dataset.py` to split the dataset.
3. Copy the split dataset to `datasets/tvb_dataset/labels` or `datasets/icable_dataset/labels`.



## Step 4: Train VSR Model

Train the VSR model and save the results:
1. Run `Step_4_VSR_Model_Training/start_training.sh` to begin training.
2. Convert checkpoints to `.pth` format by running `Step_4_VSR_Model_Training/trained_vsr_models/ckpt_to_pth.py`.
3. Copy the trained models to the directories`icable_models`, `tvb_models`, or `mixed_models`, which specify the path to the model, indicating the dataset it was trained on. (For example, if the model was trained on the TVB dataset, use `tvb`.)