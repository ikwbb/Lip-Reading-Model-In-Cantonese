export SLURM_JOB_ID=66666

cd ./auto_avsr

python train.py --exp-dir=./trained_vsr_models \
                --exp-name=cantonese_vsr \
                --modality=video \
                --root-dir=../../../datasets/tvb_dataset \
                --train-file=cstm_train.csv \
                --val-file=cstm_val.csv \
                --test-file=cstm_test.csv \
                --num-nodes=1 \
                --gpus=8 \
                --lr=0.001 \
                --max-epochs=60 \
                --max-frames=1600 \

#                --pretrained-model-path=./trained_vsr_models/cantonese_vsr_autodl_finetune_2nd_all/epoch\=20.pth