# Training Parameters

A set of default training parameters are provided in the `start_training.sh`. Their meanings are explained at the below.

- **exp-dir=./trained_vsr_models**: Directory to save checkpoints and logs.
- **exp-name=cantonese_vsr**: Experiment name, checkpoints saved at [exp_dir]/[exp_name].
- **modality=video**: Input modality type, set to video.
- **root-dir=../../../datasets/tvb_dataset**: Root directory of the preprocessed dataset.
- **train-file=cstm_train.csv**: Filename of the training label list.
- **val-file=cstm_val.csv**: Filename of the validation label list.
- **test-file=cstm_test.csv**: Filename of the testing label list.
- **num-nodes=1**: Number of machines used.
- **gpus=8**: Number of GPUs in each machine.
- **lr=0.001**: Learning rate.
- **max-epochs=60**: Number of training epochs.
- **max-frames=1600**: Maximal number of frames in a batch.