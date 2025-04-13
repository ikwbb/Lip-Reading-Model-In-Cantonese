import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('./training_dataset_tvb.csv', header=None)

# Split into train (80%) and temp (20%)
train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)

# Split temp into validation (10%) and test (10%)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

train_df.to_csv('./cstm_train.csv', index=False, header=False)
val_df.to_csv('./cstm_val.csv', index=False, header=False)
test_df.to_csv('./cstm_test.csv', index=False, header=False)

print(f"Train set: {len(train_df)} samples")
print(f"Validation set: {len(val_df)} samples")
print(f"Test set: {len(test_df)} samples")
