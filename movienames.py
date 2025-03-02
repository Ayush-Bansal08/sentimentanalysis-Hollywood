import os
import csv


def get_srt_files(folder_path):
    """
    获取指定文件夹下所有 .srt 文件的文件名列表
    （包括子文件夹中的文件）

    :param folder_path: 文件夹路径
    :return: 包含 .srt 文件名的列表
    """
    srt_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".srt"):
                srt_files.append(file)  # 仅保存文件名
    return srt_files


def save_to_csv(file_list, output_csv):
    """
    将文件名列表保存到 CSV 文件中

    :param file_list: 包含文件名的列表
    :param output_csv: 输出 CSV 文件路径
    """
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Filename"])  # 写入表头
        for name in file_list:
            writer.writerow([name])  # 写入每个文件名


# 指定文件夹路径
oscar_folder = "Oscar"  # Oscar 文件夹路径
blockbusters_folder = "Blockbusters"  # Blockbusters 文件夹路径

# 获取 .srt 文件列表
oscar_srt_files = get_srt_files(oscar_folder)
blockbusters_srt_files = get_srt_files(blockbusters_folder)

# 保存到 CSV 文件
save_to_csv(oscar_srt_files, "Oscar_srt_files.csv")
save_to_csv(blockbusters_srt_files, "Blockbusters_srt_files.csv")

print("两个 CSV 文件已生成：Oscar_srt_files.csv 和 Blockbusters_srt_files.csv")
