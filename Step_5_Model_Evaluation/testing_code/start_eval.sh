#!/bin/bash

cd auto_avsr

# Set default values
CHECK=test
SHUTDOWN=0  # Default is no shutdown

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --dataset)
            DATASET="$2"
            shift 2
            ;;
        --epoch)
            EPOCH="$2"
            shift 2
            ;;
        --lora)
            LORA="$2"
            shift 2
            ;;
        --check)
            CHECK=check
            shift
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --shutdown)
            SHUTDOWN=1  # Set shutdown flag
            shift
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Check if required parameters are provided
if [ -z "$DATASET" ] || [ -z "$EPOCH" ] || [ -z "$LORA" ] || [ -z "$MODEL" ]; then
    echo "Error: Must provide --dataset, --epoch, --lora, and --model parameters."
    exit 1
fi

# If --shutdown is specified, notify user at the start
if [ $SHUTDOWN -eq 1 ]; then
    echo "Note: The script will automatically shut down the system (60-second delay) after all tasks are completed."
fi

# Define CSV file paths
EVAL_CSV="../../testing_results/result_${DATASET}_${EPOCH}_epoch_${CHECK}.csv"
ZH_CSV="../../testing_results/zh/result_${DATASET}_${EPOCH}_epoch_${CHECK}_${LORA}_zh.csv"
FULL_CSV="../../testing_results/full/result_${DATASET}_${EPOCH}_epoch_${CHECK}_${LORA}_full.csv"

# Check and execute eval.py
if [ -f "$EVAL_CSV" ]; then
    echo "Skipping eval.py because $EVAL_CSV already exists."
else
    python eval.py --modality=video \
                   --root-dir=../../../datasets/${DATASET}_dataset \
                   --test-file=../../../datasets/${DATASET}_dataset/labels/cstm_${CHECK}.csv \
                   --pretrained-model-path=../../../${MODEL}_models/epoch\=${EPOCH}.pth \
                   --output-csv="$EVAL_CSV" | tee "../../testing_results/result_${DATASET}_${EPOCH}_epoch_${CHECK}_${LORA}.txt"
    if [ $? -ne 0 ]; then
        echo "eval.py execution failed, exiting script."
        exit 1
    fi
fi

# Check and execute generate_zh.py
if [ -f "$ZH_CSV" ]; then
    echo "Skipping generate_zh.py because $ZH_CSV already exists."
else
    python ../generate_zh.py --lora ${LORA} \
                             --input_csv "$EVAL_CSV" \
                             --output_csv "$ZH_CSV"
    if [ $? -ne 0 ]; then
        echo "generate_zh.py execution failed, exiting script."
        exit 1
    fi
fi

# Check and execute generate_full_manifest.py
if [ -f "$FULL_CSV" ]; then
    echo "Skipping generate_full_manifest.py because $FULL_CSV already exists."
else
    python ../generate_full_manifest.py --ground_truth ${DATASET} \
                                        --zh_csv "$ZH_CSV" \
                                        --index_csv ../../../datasets/${DATASET}_dataset/labels/cstm_${CHECK}.csv \
                                        --output_csv "$FULL_CSV"
    if [ $? -ne 0 ]; then
        echo "generate_full_manifest.py execution failed, exiting script."
        exit 1
    fi
fi

# After all tasks are completed, check if shutdown is required
if [ $SHUTDOWN -eq 1 ]; then
    echo "All tasks completed, system will shut down in 60 seconds..."
    /usr/bin/shutdown -h +1
fi