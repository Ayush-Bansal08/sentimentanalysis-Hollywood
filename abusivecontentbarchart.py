import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from transformers import pipeline

def count_abusive_content(file_paths, content_analyzer):
    abusive_count = 0

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split content into segments by double newlines (srt block format)
        segments = content.strip().split("\n\n")

        for segment in segments:
            # Extract the textual part of the subtitle block
            lines = segment.split("\n")
            if len(lines) > 2:  # Skip blocks without text
                text = " ".join(lines[2:])
                # Analyze the text for abusive content
                results = content_analyzer(text, truncation=True, max_length=512)
                for result in results:
                    if result['label'].lower() == 'offensive' and result['score'] > 0.5:  # Threshold for confidence
                        abusive_count += 1

    return abusive_count

def calculate_yearly_abusive_counts(folder_path, content_analyzer):
    yearly_counts = {}

    for year in range(1950, 2025):
        year_folder = os.path.join(folder_path, str(year))
        if os.path.exists(year_folder):
            file_paths = glob.glob(os.path.join(year_folder, '*.srt'))
            if file_paths:
                yearly_counts[year] = count_abusive_content(file_paths, content_analyzer)

    return yearly_counts

def plot_abusive_counts_by_year(oscar_yearly_counts, blockbusters_yearly_counts):
    # Extract data for plotting
    years = list(range(1950, 2025))
    oscar_counts = [oscar_yearly_counts.get(year, 0) for year in years]
    blockbusters_counts = [blockbusters_yearly_counts.get(year, 0) for year in years]

    # Plot settings
    x_indices = np.arange(len(years))  # One bar per year
    bar_width = 0.35

    plt.figure(figsize=(20, 8))  # Wider figure to accommodate all years

    # Plot Oscar and Blockbusters bars
    plt.bar(x_indices - bar_width / 2, oscar_counts, width=bar_width, color='blue', label='Oscar', alpha=0.7)
    plt.bar(x_indices + bar_width / 2, blockbusters_counts, width=bar_width, color='orange', label='Blockbusters', alpha=0.7)

    # Set x-ticks and labels
    plt.xticks(x_indices, years, fontsize=16)
    plt.yticks(fontsize=16)
    plt.xlabel('Year', fontsize=16)
    plt.ylabel('Abusive Content Count', fontsize=16)

    # Highlight key years
    key_years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    plt.xticks([x_indices[years.index(y)] for y in key_years], key_years, fontsize=16)

    # Add legend and grid
    plt.legend(fontsize=15)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Initialize Hugging Face content analysis pipeline
    content_analyzer = pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-offensive')

    # Define paths for Oscar and Blockbusters datasets
    oscar_path = './Oscar'
    blockbusters_path = './Blockbusters'

    # Calculate yearly abusive content counts
    oscar_yearly_counts = calculate_yearly_abusive_counts(oscar_path, content_analyzer)
    blockbusters_yearly_counts = calculate_yearly_abusive_counts(blockbusters_path, content_analyzer)

    # Plot the abusive content trends by year
    plot_abusive_counts_by_year(oscar_yearly_counts, blockbusters_yearly_counts)
