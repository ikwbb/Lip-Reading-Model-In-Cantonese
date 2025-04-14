# Filename conventions

This directory contains result files generated from a Visual Speech Recognition (VSR) model evaluated on different test sets. The filenames follow a consistent naming convention that encodes key information about the training setup, evaluation data, and experimental configuration.



## Filename Format

```
result_{testset}_{epoch}_epoch_test_{jyutping_variant}_full{_word_segmented}.csv
```



## Filename Components

| Component            | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| `{testset}`          | Indicates which test set the model was evaluated on: <br />`tvb`: tested on the TVB test set <br />`icable`: tested on the iCable test set |
| `{epoch}_epoch`      | The number of training epochs the model underwent before evaluation |
| `{jyutping_variant}` | Specifies the type of jyutping used during decoding: <br />`absolute`: standard, unambiguous jyutping <br />`ambiguous`: a deprecated variant that allows phonetic overlap, used in an attempt to reduce reliance on lip shape alone and shift contextual disambiguation to the language model |
| {_word_segmented}    | If `_word_segmented` exists, Cantonese sentences are segmented into words for calculating Word Error Rate (WER). The sentence will be segmented by space, which will be stored in column `predicted_cantonese_word_segmented` and `transcript_trad_word_segmented`.<br /><br />Original: 排名全球第六<br />Word Segmented: 排名 全球 第六<br /> |



## Training Details

- **Epoch ≤ 75**: Models were trained on the **TVB-only** training set.
- **Epoch > 75**: Models were trained on a **TVB + iCable mixed** training set. Specifically:
  - Epochs 1–75: TVB training data
  - Epochs 76–135: Mixed TVB + iCable training data



## Word Segmentation for WER Calculation

The Jupyter Notebook `Word Segmentation.ipynb` performs **word segmentation** as a preprocessing step for calculating the **Word Error Rate (WER)**. The segmentation method used is aligned with the evaluation approach described in [Xiao et al.](https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/ipr2.13123), which ensures consistency and comparability with their results.



## Additional Notes

- Files with the prefix `(with_pretrained_model)` or `(without_pretrained_model)` indicate whether a pretrained model was used during training.
- The `ambiguous` variant was an experimental approach that has since been deprecated.