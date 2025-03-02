import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from transformers import pipeline
from collections import defaultdict

def count_abusive_content_in_category(year_folder, category_folder, content_analyzer):
    abusive_counts = []
    # 获取某类别的所有电影名称
    category_files = set(os.path.basename(f) for f in glob.glob(os.path.join(category_folder, '*.srt')))
    year_files = glob.glob(os.path.join(year_folder, '*.srt'))

    for file_path in year_files:
        movie_name = os.path.basename(file_path)
        if movie_name in category_files:  # 确认电影属于该类别
            abusive_count = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            segments = content.strip().split("\n\n")
            for segment in segments:
                lines = segment.split("\n")
                if len(lines) > 2:
                    text = " ".join(lines[2:])
                    results = content_analyzer(text, truncation=True, max_length=512)
                    abusive_count += sum(1 for result in results if result['label'].lower() == 'offensive' and result['score'] > 0.5)
            abusive_counts.append(abusive_count)

    return abusive_counts

def calculate_decadal_abusive_stats(year_folder, category_folders, content_analyzer):
    decadal_stats = {decade: {category: {'counts': [], 'avg': 0, 'std': 0} for category in category_folders.keys()} for decade in range(1950, 2030, 10)}

    for year in range(1950, 2025):
        year_folder_path = os.path.join(year_folder, str(year))
        if os.path.exists(year_folder_path):
            decade = (year // 10) * 10
            for category, category_folder in category_folders.items():
                abusive_counts = count_abusive_content_in_category(year_folder_path, category_folder, content_analyzer)
                decadal_stats[decade][category]['counts'].extend(abusive_counts)

    # Calculate average and std for each category per decade
    for decade, categories in decadal_stats.items():
        for category, stats in categories.items():
            counts = stats['counts']
            if counts:
                stats['avg'] = np.mean(counts)
                stats['std'] = np.std(counts)

    return decadal_stats

def plot_decadal_abusive_stats(decadal_stats):
    decades = sorted(decadal_stats.keys())
    categories = list(next(iter(decadal_stats.values())).keys())
    colors = ['blue', 'orange', 'green', 'red']

    x_indices = np.arange(len(decades))
    bar_width = 0.2

    plt.figure(figsize=(16, 8))

    for i, category in enumerate(categories):
        averages = [decadal_stats[decade][category]['avg'] for decade in decades]
        std_devs = [decadal_stats[decade][category]['std'] for decade in decades]
        plt.bar(x_indices + i * bar_width, averages, width=bar_width, label=category, color=colors[i], alpha=0.7, yerr=std_devs, capsize=5)

    # 设置横轴和标签
    plt.xticks(x_indices + bar_width * (len(categories) - 1) / 2, [f"{d}s" for d in decades], fontsize=16)
    plt.xlabel("Year", fontsize=16)
    plt.ylabel("Average Abusive Content", fontsize=16)
    plt.legend(fontsize=15)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 初始化 Hugging Face 内容分析模型
    content_analyzer = pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-offensive')

    # 设置文件夹路径
    year_folder = './Year'
    category_folders = {
        'Action': './Category/Action',
        'Comedy': './Category/Comedy',
        'Drama': './Category/Drama',
        'Thriller': './Category/Thriller'
    }

    # 计算每十年中各类别的 abusive content 平均数和标准差
    decadal_stats = calculate_decadal_abusive_stats(year_folder, category_folders, content_analyzer)

    # 绘制柱状图
    plot_decadal_abusive_stats(decadal_stats)
