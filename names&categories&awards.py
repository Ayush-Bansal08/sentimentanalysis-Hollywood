import os

# 定义主目录和输出文件
folders = ["Blockbusters", "Oscar"]  # 你的 Blockbusters 和 Oscar 文件夹路径
output_file = "movie_titles_with_awards.txt"

# 创建一个空的列表用于存储结果
movie_titles = []

# 遍历每个奖项文件夹
for folder in folders:
    for year_folder in os.listdir(folder):  # 遍历年份文件夹
        year_folder_path = os.path.join(folder, year_folder)
        if os.path.isdir(year_folder_path):  # 确保是文件夹
            for file in os.listdir(year_folder_path):  # 遍历.srt文件
                if file.endswith(".srt"):  # 检查文件扩展名
                    movie_name = os.path.splitext(file)[0]  # 去掉扩展名
                    movie_titles.append(f"{movie_name} ({year_folder}, {folder})")

# 将结果写入txt文件
with open(output_file, "w", encoding="utf-8") as f:
    for title in movie_titles:
        f.write(title + "\n")

print(f"提取完成，所有电影名称已保存到 {output_file}")
