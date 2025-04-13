import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser(description="Merge CSV files based on ground truth and video paths.")
    parser.add_argument('--ground_truth', required=True, choices=['tvb', 'icable'], 
                        help="Specify the ground truth CSV: 'tvb' or 'icable'")
    parser.add_argument('--zh_csv', required=True, 
                        help="Path to the zh_csv file")
    parser.add_argument('--index_csv', required=True, 
                        help="Path to the index_csv file")
    parser.add_argument('--output_csv', required=True, 
                        help="Path to the output CSV file")
    args = parser.parse_args()

    
    # Dataset Selection: TVB or iCable
    if args.ground_truth == 'tvb':
        gt_path = '../../datasets/ground_truth_labels/tvb_gt.csv'
    elif args.ground_truth == 'icable':
        gt_path = '../../datasets/ground_truth_labels/icable_gt.csv'

    
    df_gt = pd.read_csv(gt_path)  
    df_zh = pd.read_csv(args.zh_csv)  
    df_index = pd.read_csv(args.index_csv, header=None, 
                           names=['dataset_name', 'video_path', 'input_length', 'tokens'])  

    
    df_merged = pd.concat([df_zh, df_index], axis=1)
    df_merged['video_id'] = df_merged['video_path'].apply(lambda x: x.split('/')[-1].split('.')[0])
    df_final = pd.merge(df_merged, df_gt, on='video_id', how='left')

    desired_columns = [
        'index', 'prediction', 'ground_truth', 'transcript_trad', 
        'predicted_cantonese', 'video_id', 'tokens', 'video_path'
    ]
    
    for col in desired_columns:
        if col not in df_final.columns:
            print(f"Warning: Column '{col}' not found in the merged DataFrame.")

    df_final = df_final[desired_columns]
    df_final.to_csv(args.output_csv, index=False)
    print(f"Output CSV Saved to: {args.output_csv}")

if __name__ == '__main__':
    main()