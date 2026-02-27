"""
文件夹/文件创建工具

功能:
    用于创建文件夹/文件,当文件夹/文件不存在时,创建;
"""

import os


def create_folder(path):
    """
    创建文件夹

    参数:
        path (str): 文件夹路径
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"文件夹已创建: {path}")
    else:
        print(f"文件夹已存在: {path}")


def create_file(path):
    """
    创建文件

    参数:
        path (str): 文件路径
    """
    directory = os.path.dirname(path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"文件夹已创建: {directory}")

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            pass
        print(f"文件已创建: {path}")
    else:
        print(f"文件已存在: {path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python create_folder.py <type> <path>")
        print("type: folder 或 file")
        sys.exit(1)

    item_type = sys.argv[1]
    item_path = sys.argv[2]

    if item_type == "folder":
        create_folder(item_path)
    elif item_type == "file":
        create_file(item_path)
    else:
        print("错误: type 必须是 'folder' 或 'file'")
        sys.exit(1)
