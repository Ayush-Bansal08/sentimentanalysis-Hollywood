import os
import pandas as pd
import shutil


def copy_oscar_srt_files():
    # 读取CSV文件
    try:
        df = pd.read_csv('Blockbusters_srt_files.csv')
        oscar_files = set(name.lower() for name in df['Filename'])
        print(f"Found {len(oscar_files)} files in the CSV file")
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # 源文件夹和目标文件夹名称
    categories = ['Action', 'Comedy', 'Drama', 'Thriller']
    source_base = 'Category'
    dest_base = 'Blockbusters'

    # 检查源文件夹是否存在
    if not os.path.exists(source_base):
        print(f"Error: Source directory '{source_base}' not found!")
        return

    # 创建目标文件夹结构
    if not os.path.exists(dest_base):
        os.makedirs(dest_base)
        print(f"Created destination directory: {dest_base}")

    for category in categories:
        dest_path = os.path.join(dest_base, category)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
            print(f"Created subdirectory: {dest_path}")

    # 记录处理的文件
    processed_files = set()
    missing_files = set()

    # 处理每个类别文件夹
    for category in categories:
        source_path = os.path.join(source_base, category)
        dest_path = os.path.join(dest_base, category)

        if not os.path.exists(source_path):
            print(f"Source category folder not found: {source_path}")
            continue

        print(f"\nProcessing {category} folder...")

        # 遍历当前文件夹中的文件
        try:
            for filename in os.listdir(source_path):
                if filename.lower() in oscar_files:
                    source_file = os.path.join(source_path, filename)
                    dest_file = os.path.join(dest_path, filename)

                    try:
                        shutil.copy2(source_file, dest_file)
                        processed_files.add(filename.lower())
                        print(f"✓ Copied: {filename} to {category} category")
                    except Exception as e:
                        print(f"✗ Error copying {filename}: {e}")
        except Exception as e:
            print(f"✗ Error accessing {source_path}: {e}")

    # 检查未找到的文件
    missing_files = oscar_files - processed_files
    if missing_files:
        print("\nWarning: The following files from the CSV were not found:")
        for file in sorted(missing_files):
            print(f"- {file}")

    print(f"\nProcessing complete!")
    print(f"Successfully processed: {len(processed_files)} files")
    print(f"Missing files: {len(missing_files)} files")


if __name__ == "__main__":
    copy_oscar_srt_files()
