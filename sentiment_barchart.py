import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from transformers import pipeline

def calculate_awss(file_paths, emotion_analyzer, weights):
  
    awss_values = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Analyze emotions
        emotions = emotion_analyzer(content, truncation=True, max_length=512)
        weighted_scores = []
        for emotion in emotions:
            label = emotion['label'].lower()
            score = emotion['score']
            weighted_score = weights.get(label, 0) * score
            weighted_scores.append(weighted_score)

        if weighted_scores:
            awss_values.append(np.mean(weighted_scores))

    return np.mean(awss_values) if awss_values else 0

def calculate_yearly_awss(folder_path, emotion_analyzer, weights):
 
    yearly_awss = {}

    for year in range(1950, 2025):
        year_folder = os.path.join(folder_path, str(year))
        if os.path.exists(year_folder):
            file_paths = glob.glob(os.path.join(year_folder, '*.srt'))
            if file_paths:
                yearly_awss[year] = calculate_awss(file_paths, emotion_analyzer, weights)

    return yearly_awss

def calculate_decadal_awss(yearly_awss):

    decadal_awss = {}

    for start_year in range(1950, 2030, 10):
        end_year = start_year + 9 if start_year < 2020 else 2024
        decade_years = [year for year in range(start_year, end_year + 1) if year in yearly_awss]

        if decade_years:
            decade_values = [yearly_awss[year] for year in decade_years]
            decadal_awss[start_year] = np.mean(decade_values)

    return decadal_awss

def plot_awss_with_error_bars(decadal_awss1, decadal_awss2):
    decades1, values1 = zip(*sorted(decadal_awss1.items()))
    decades2, values2 = zip(*sorted(decadal_awss2.items()))

    x_indices1 = np.arange(len(decades1))
    x_indices2 = np.arange(len(decades2)) + 0.4  # Offset for the second bar

    plt.figure(figsize=(12, 6))
    plt.bar(x_indices1, values1, width=0.4, color='blue', label='Oscar', capsize=5)
    plt.bar(x_indices2, values2, width=0.4, color='orange', label='Blockbusters', capsize=5)

    plt.xticks(x_indices1 + 0.2, [f"{int(d)}s" for d in decades1])  # Center labels
    plt.xlabel('Decade', fontsize=14)
    plt.ylabel('Average Weighted Sentiment Score', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Initialize Hugging Face emotion analysis pipeline
    emotion_analyzer = pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-emotion')

    # Define weights for emotions

    weights = {
        'denial': -4,
        'pessimistic': -3,
        'sad': -2,
        'anxious': -2,
        'humour': 1,
        'thankful': 2,
        'optimistic': 3
    }



    # Define paths for Oscar and Blockbusters datasets
    oscar_path = './Oscar'
    blockbusters_path = './Blockbusters'

    # Calculate yearly AWSS values
    oscar_yearly_awss = calculate_yearly_awss(oscar_path, emotion_analyzer, weights)
    blockbusters_yearly_awss = calculate_yearly_awss(blockbusters_path, emotion_analyzer, weights)

    # Calculate decadal AWSS values
    oscar_decadal_awss = calculate_decadal_awss(oscar_yearly_awss)
    blockbusters_decadal_awss = calculate_decadal_awss(blockbusters_yearly_awss)

    # Plot the AWSS trends with error bars
    plot_awss_with_error_bars(oscar_decadal_awss, blockbusters_decadal_awss)

