import os


def get_code_language(ext):
    mapping = {".java": "java", ".kts": "kotlin", ".groovy": "groovy", ".xml": "xml"}
    return mapping.get(ext, "")


def process_directory(current_dir, base_dir, outfile, valid_extensions):
    """递归遍历当前目录下所有文件，并写入符合条件的内容到 outfile。"""
    for entry in os.listdir(current_dir):
        full_path = os.path.join(current_dir, entry)
        if os.path.isdir(full_path):
            # 如果是目录则递归调用
            process_directory(full_path, base_dir, outfile, valid_extensions)
        else:
            ext = os.path.splitext(entry)[1].lower()
            if ext not in valid_extensions:
                continue

            # 获取相对于 base_dir 的路径作为标题
            rel_path = os.path.relpath(full_path, base_dir)
            try:
                with open(full_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
            except Exception as e:
                print(f"Error reading {full_path}: {e}")
                continue

            # 写入标题
            outfile.write(f"\n# {rel_path}\n")
            if ext == ".md":
                # 对于 md 文件，直接插入内容
                outfile.write(content)
                outfile.write("\n")
            else:
                # 对于代码文件，按格式写入代码块
                language = get_code_language(ext)
                outfile.write(f"```{language}\n")
                outfile.write(content)
                outfile.write("\n```\n")


def main():
    base_dir = "intellij-sdk-code-samples"
    output_file = "intellij-sdk-code-samples.md"
    valid_extensions = {".md", ".java", ".kts", ".groovy", ".xml"}

    with open(output_file, "w", encoding="utf-8") as outfile:
        process_directory(base_dir, base_dir, outfile, valid_extensions)

    print(f"合并完成，生成文件：{output_file}")


if __name__ == "__main__":
    main()
