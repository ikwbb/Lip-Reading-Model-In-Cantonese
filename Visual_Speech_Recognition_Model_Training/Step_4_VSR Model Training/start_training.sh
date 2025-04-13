export SLURM_JOB_ID=66666

cd ./auto_avsr

python train.py --exp-dir=/root/autodl-tmp/exp_finetune \
                --exp-name=cantonese_vsr \
                --modality=video \
                --root-dir=/root/autodl-tmp/all_dataset \
                --train-file=all_train_shuffled.csv \
                --val-file=all_val_shuffled.csv \
                --test-file=all_test_shuffled.csv \
                --num-nodes=1 \
                --gpus=8 \
                --lr=0.001 \
                --max-epochs=60 \
                --max-frames=1600 \

#                --pretrained-model-path=/root/autodl-tmp/exp_finetune/cantonese_vsr_autodl_finetune_2nd_all/epoch\=20.pth