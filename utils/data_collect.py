import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class FileAggregator:
    """
    文件整合工具类
    用于遍历指定文件夹，整合.vue和.js文件内容，并显示目录结构
    """

    def __init__(self, folder_path: str):
        """
        初始化工具类

        Args:
            folder_path (str): 要遍历的文件夹路径
        """
        self.folder_path = Path(folder_path)
        self.target_extensions = {'.vue', '.js', ".py"}
        self.file_contents = {}
        self.directory_structure = []

        # 排除文件夹配置 - 可以在这里添加要排除的文件夹名称
        self.excluded_folders = [
            'node_modules',
            '.git',
            '.vscode',
            '.idea',
            'dist',
            'build',
            'coverage',
            '.nuxt',
            '.next',
            'vendor',
            '__pycache__',
            '.pytest_cache',
            'logs',
            'tmp',
            'temp'
        ]

    def is_excluded_folder(self, folder_path: Path) -> bool:
        """
        判断文件夹是否在排除列表中

        Args:
            folder_path (Path): 文件夹路径

        Returns:
            bool: 是否应该排除该文件夹
        """
        folder_name = folder_path.name.lower()
        return folder_name in [excluded.lower() for excluded in self.excluded_folders]

    def is_target_file(self, file_path: Path) -> bool:
        """
        判断文件是否为目标文件类型

        Args:
            file_path (Path): 文件路径

        Returns:
            bool: 是否为.vue或.js文件
        """
        return file_path.suffix.lower() in self.target_extensions

    def read_file_content(self, file_path: Path) -> Optional[str]:
        """
        读取文件内容

        Args:
            file_path (Path): 文件路径

        Returns:
            Optional[str]: 文件内容，读取失败返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as file:
                    return file.read()
            except Exception as e:
                print(f"读取文件失败 {file_path}: {e}")
                return None
        except Exception as e:
            print(f"读取文件失败 {file_path}: {e}")
            return None

    def build_tree_structure(self, path: Path, prefix: str = "", is_last: bool = True) -> List[str]:
        """
        构建树状目录结构

        Args:
            path (Path): 当前路径
            prefix (str): 前缀字符串
            is_last (bool): 是否为最后一个项目

        Returns:
            List[str]: 目录结构行列表
        """
        if not path.exists():
            return [f"{prefix}[目录不存在: {path}]"]

        lines = []

        # 添加当前目录/文件
        connector = "└── " if is_last else "├── "
        name = path.name

        # 标记排除的文件夹
        if path.is_dir() and self.is_excluded_folder(path):
            name += " [已排除]"
        elif path.is_file() and self.is_target_file(path):
            name += " [目标文件]"

        lines.append(f"{prefix}{connector}{name}")

        # 如果是目录且不在排除列表中，递归处理子项目
        if path.is_dir() and not self.is_excluded_folder(path):
            try:
                children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))

                for i, child in enumerate(children):
                    is_child_last = i == len(children) - 1
                    child_prefix = prefix + ("    " if is_last else "│   ")
                    lines.extend(self.build_tree_structure(child, child_prefix, is_child_last))

            except PermissionError:
                lines.append(f"{prefix}    [权限不足]")

        return lines

    def scan_directory(self):
        """
        扫描目录并整合文件内容（排除指定文件夹）
        """
        if not self.folder_path.exists():
            print(f"错误: 目录 '{self.folder_path}' 不存在")
            return

        if not self.folder_path.is_dir():
            print(f"错误: '{self.folder_path}' 不是一个目录")
            return

        print(f"开始扫描目录: {self.folder_path}")
        print(f"排除文件夹: {', '.join(self.excluded_folders)}")
        print("=" * 50)

        # 遍历所有文件，但排除指定文件夹
        for root, dirs, files in os.walk(self.folder_path):
            root_path = Path(root)

            # 排除指定的文件夹（修改dirs列表以避免进入这些目录）
            dirs_to_remove = []
            for dir_name in dirs:
                dir_path = root_path / dir_name
                if self.is_excluded_folder(dir_path):
                    dirs_to_remove.append(dir_name)

            # 从dirs中移除要排除的文件夹
            for dir_name in dirs_to_remove:
                dirs.remove(dir_name)
                print(f"跳过排除文件夹: {root_path / dir_name}")

            # 处理文件
            for file in files:
                file_path = root_path / file

                if self.is_target_file(file_path):
                    relative_path = file_path.relative_to(self.folder_path)
                    content = self.read_file_content(file_path)

                    if content is not None:
                        self.file_contents[str(relative_path)] = content
                        print(f"已读取: {relative_path}")

    def print_directory_structure(self):
        """
        打印目录结构
        """
        print("\n" + "=" * 50)
        print("目录结构:")
        print("=" * 50)

        structure_lines = self.build_tree_structure(self.folder_path)
        for line in structure_lines:
            print(line)

    def print_file_contents(self):
        """
        打印所有目标文件的内容
        """
        print("\n" + "=" * 50)
        print("文件内容整合:")
        print("=" * 50)

        if not self.file_contents:
            print("没有找到任何.vue或.js文件")
            return

        for file_path, content in self.file_contents.items():
            print(f"\n{'=' * 20} {file_path} {'=' * 20}")
            print(content)
            print("=" * (42 + len(file_path)))

    def save_aggregated_content(self, output_file: str = "aggregated_files.txt"):
        """
        将整合的内容保存到文件

        Args:
            output_file (str): 输出文件名
        """
        try:
            # 确保输出目录存在
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("文件整合报告\n")
                f.write(f"源目录: {self.folder_path.absolute()}\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"排除文件夹: {', '.join(self.excluded_folders)}\n")
                f.write("=" * 50 + "\n\n")

                # 写入目录结构
                f.write("目录结构:\n")
                f.write("-" * 30 + "\n")
                structure_lines = self.build_tree_structure(self.folder_path)
                for line in structure_lines:
                    f.write(line + "\n")

                f.write("\n" + "=" * 50 + "\n")
                f.write("文件内容:\n")
                f.write("=" * 50 + "\n")

                # 写入文件内容
                if not self.file_contents:
                    f.write("没有找到任何.vue或.js文件\n")
                else:
                    for file_path, content in self.file_contents.items():
                        f.write(f"\n{'=' * 20} {file_path} {'=' * 20}\n")
                        if content:
                            f.write(content)
                        else:
                            f.write("[文件内容为空]\n")
                        f.write(f"\n{'=' * (42 + len(file_path))}\n")

            print(f"\n整合内容已保存到: {Path(output_file).absolute()}")

        except PermissionError:
            print(f"保存文件失败: 没有写入权限，请检查文件路径和权限设置")
        except FileNotFoundError:
            print(f"保存文件失败: 指定的路径不存在")
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            print(f"错误类型: {type(e).__name__}")

    def run(self, save_to_file: bool = False, output_file: str = "aggregated_files.txt"):
        """
        运行完整的文件整合流程

        Args:
            save_to_file (bool): 是否保存到文件
            output_file (str): 输出文件名
        """
        # 扫描目录
        self.scan_directory()

        # 打印目录结构
        self.print_directory_structure()

        # 打印文件内容
        self.print_file_contents()

        # 保存到文件（可选）
        if save_to_file:
            self.save_aggregated_content(output_file)

        # 统计信息
        print(f"\n{'=' * 50}")
        print("统计信息:")
        print(f"共找到 {len(self.file_contents)} 个目标文件")
        print(f"目标文件类型: {', '.join(self.target_extensions)}")
        print(f"排除文件夹: {', '.join(self.excluded_folders)}")


# 使用示例
if __name__ == "__main__":
    # 创建工具实例
    folder_name = input("请输入文件夹路径: ").strip()

    if not folder_name:
        folder_name = r"D:\code\project\fast_api_admin_frontend\src\views\api_test_cases"  # 默认当前目录
        # folder_name = r"D:\code\project\fast_api_admin\module_fastmcp"  # 默认当前目录
        # folder_name = r"D:\code\project\fast_api_admin\module_fastmcp"  # 默认当前目录

    aggregator = FileAggregator(folder_name)

    # 询问是否保存到文件
    save_choice = input("是否保存整合结果到文件? (y/N): ").strip().lower()
    if not save_choice:
        save_choice = "y"
    save_to_file = save_choice in ['y', 'yes', '是']

    # 运行整合流程
    aggregator.run(save_to_file=save_to_file)
