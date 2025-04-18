# Lip-Reading Model In Cantonese



### Model Evaluation

Please check this [Jupyter Notebook](https://github.com/ikwbb/Lip-Reading-Model-In-Cantonese/blob/main/Step_5_Model_Evaluation/testing_results/full/Model%20Evaluation.ipynb) for detailed model evaluation results.

---



### Code Implementation

This repository presents a complete pipeline for building a Cantonese lip-reading system. The project is organized into five main stages, each of which is contained within a corresponding folder:

1. `Step_1_News_Videos_Scraping`
2. `Step_2_News_Videos_Preprocessing`
3. `Step_3_Visual_Speech_Recognition_Model_Training`
4. `Step_4_Large_Language_Model_Fine_Tuning`
5. `Step_5_Model_Evaluation`



Please navigate through each folder in sequence to explore the full workflow.

------

### Step 1: News Videos Scraping

<div align="center"><img src="./assets/step-1.png" alt="Step 1" style="zoom:60%;" /></div>

This step provides the code used to scrape news videos from TVB and iCable. The videos serve as the primary dataset for subsequent processing and training.

------

### Step 2: News Videos Preprocessing

![Step 2](./assets/step-2.png)

In this step, the scraped news videos are preprocessed to extract the mouth region of interest (ROI) and align the corresponding transcription. This forms the foundation for the visual speech recognition stage.

#### Dataset Download
The preprocessed and manifested dataset can be found in the following:
| Dataset | Size | Link |
|---------|------|------|
|TVB & iCable Dataset | 115GB | [Link](https://1drv.ms/f/c/DADC679B5C6EBC0F/EsKbtspvEilFpx5OoSefZIUBZJIoRAAIpFm_SMktOWD4kw?e=Eg0lpb) |


#### Sample: Original News Clip - TVB Dataset
https://github.com/user-attachments/assets/b67838f8-f8e3-4a90-9949-c5729ee96fe5

#### Sample: Preprocessed Mouth Region of Interest (ROI) - TVB Dataset
https://github.com/user-attachments/assets/d3874cf0-016a-4a86-bd1b-8f975a046019

#### Sample: Original News Clip - iCable Dataset
https://github.com/user-attachments/assets/a3f6d0f7-abbd-4b71-a2ad-6d9af432c856

#### Sample: Preprocessed Mouth Region of Interest (ROI) - iCable Dataset
https://github.com/user-attachments/assets/d40fb1c2-a5e1-440f-90f6-408a046473a9




------

### Step 3: Visual Speech Recognition (VSR) Model Training

![Step 3](./assets/step-3.png)

This stage contains the training pipeline for the Visual Speech Recognition model, which maps the mouth ROI sequences to toneless Jyutping sequences representing spoken Cantonese.

------

### Step 4: Large Language Model (LLM) Fine-Tuning

![Step 4](./assets/step-4.png)

Here, a Large Language Model is fine-tuned to convert the output Jyutping sequences from the VSR model into fluent Cantonese sentences.

------

### Step 5: Model Evaluation

This section includes all testing scripts and evaluation results. It demonstrates the final system’s performance and provides insights into model accuracy and areas for improvement.
