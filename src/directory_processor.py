import os
from typing import List, Dict
from loguru import logger
from multiprocessing import Pool
from parsers.java.java_parser import parse_java_file
from parsers.kotlin.kotlin_parser import parse_kotlin_file


def parse_file(args) -> tuple[str, List[Dict], str]:
    """Worker function to parse a single file."""
    full_path, source_dir = args
    try:
        with open(full_path, "r", encoding="utf-8") as infile:
            content = infile.read()

        rel_path = os.path.relpath(full_path, source_dir)
        formatted_path = rel_path.replace("/", ".")

        if full_path.endswith(".java"):
            class_info = parse_java_file(content)
        else:
            class_info = parse_kotlin_file(content)

        return formatted_path, class_info, ""
    except Exception as e:
        return formatted_path, None, str(e)


def count_source_files(source_dir: str) -> int:
    """Count total number of Java and Kotlin files in the source directory."""
    total_count = 0
    for root, _, files in os.walk(source_dir):
        total_count += sum(1 for file in files if file.endswith((".java", ".kt")))
    return total_count


class MarkdownWriter:
    def __init__(self, base_filename: str, max_lines: int = 500000):
        self.base_filename = base_filename
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        self.max_lines = max_lines
        self.current_file = None
        self.current_lines = 0
        self.file_counter = 1
        self.buffer = []
        self._open_new_file()

    def _open_new_file(self):
        if self.current_file:
            filename = self.current_file.name
            self.current_file.close()
            logger.info(
                f"Completed writing {filename} with {self._count_lines(filename)} lines"
            )
        filename = f"{self.base_filename}-{self.file_counter}.md"
        filepath = os.path.join(self.output_dir, filename)
        self.current_file = open(filepath, "w", encoding="utf-8")
        self.current_lines = 0
        self.file_counter += 1
        # Write introduction in each file
        intro_text = "这个文件里包含所有ideaIC-2024.2的源代码，里面的java类、函数、kotlin类和函数，可以用来帮助实现intellij plugin\n\n"
        self.current_file.write(intro_text)
        self.current_lines += intro_text.count("\n") + 1

    def _count_lines(self, file_path: str) -> int:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)

    def write_class_info(self, class_path: str, class_info: List[Dict]):
        content = f"\n## {class_path}\n\n"

        for class_data in class_info:
            content += f"### Class: {class_data['name']}\n\n"

            # Write constants table
            if class_data["constants"]:
                content += "| Constant | Comment |\n|----------|---------|\n"
                for const in class_data["constants"]:
                    comment = const["comment"].replace("\n", " ").strip()
                    content += f"| {const['name']} | {comment} |\n"
                content += "\n"

            # Write methods table
            if class_data["methods"]:
                content += "| Method | Comment |\n|---------|---------|\n"
                for method in class_data["methods"]:
                    comment = method["comment"].replace("\n", " ").strip()
                    content += f"| {method['name']} | {comment} |\n"
                content += "\n"

        self.write(content)

    def write(self, content: str):
        lines = content.split("\n")
        total_lines = self.current_lines + len(self.buffer) + len(lines)

        if total_lines >= self.max_lines:
            self._write_buffer()
            if self.current_lines + len(lines) >= self.max_lines:
                self._open_new_file()

        self.buffer.extend(lines)
        if not any(line.startswith("```") for line in self.buffer[-3:]):
            self._write_buffer()

    def _write_buffer(self):
        if not self.buffer:
            return
        content = "\n".join(self.buffer)
        self.current_file.write(content + "\n")
        self.current_lines += content.count("\n") + 1
        self.buffer = []

        if self.current_lines >= self.max_lines:
            self._open_new_file()

    def close(self):
        self._write_buffer()
        if self.current_file:
            filename = self.current_file.name
            self.current_file.close()
            logger.info(
                f"Completed writing {filename} with {self._count_lines(filename)} lines"
            )


def process_directory(
    source_dir: str,
    base_output_file: str,
    max_lines: int = 100000,
    worker_num: int = 10,
):
    """Process a directory containing Java and Kotlin files and generate markdown documentation."""
    # First count total files to process
    total_files = count_source_files(source_dir)
    logger.info(f"Found {total_files} Java and Kotlin files to process")

    writer = MarkdownWriter(base_output_file, max_lines)
    processed_files = 0
    last_progress_milestone = -1

    # Collect all files to process
    files_to_process = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith((".java", ".kt")):
                full_path = os.path.join(root, file)
                files_to_process.append((full_path, source_dir))

    # Process files in parallel
    with Pool(processes=worker_num) as pool:
        for formatted_path, class_info, error in pool.imap_unordered(
            parse_file, files_to_process
        ):
            processed_files += 1
            if error:
                logger.error(f"Error processing {formatted_path}: {error}")
            elif class_info:
                writer.write_class_info(formatted_path, class_info)

            current_progress = int((processed_files / total_files) * 1000)
            if current_progress > last_progress_milestone:
                logger.info(
                    f"Progress: {current_progress / 10:.1f}% ({processed_files}/{total_files} files)"
                )
                last_progress_milestone = current_progress

    writer.close()
    logger.info(f"Markdown files generated with base name: {base_output_file}")
