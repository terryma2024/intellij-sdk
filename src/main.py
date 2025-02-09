from loguru import logger
import sys
from directory_processor import process_directory
from parsers.kotlin.kotlin_parser import parse_kotlin_file


def setup_logger():
    """Configure the logger with project settings"""
    # Remove default handler
    logger.remove()

    # Add custom handler with project settings
    logger.add(sys.stderr, level="INFO", colorize=True)
    # Configure logger to write errors to error.log
    logger.add(
        "error.log", format="{time} {level} {message}", level="ERROR", rotation="1 day"
    )


def main():
    file = "/Users/bytedance/Projects/ideaIC-2024.2-sources/com/intellij/ide/GeneralSettings.kt"
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
        class_info = parse_kotlin_file(content)
        print(class_info)


def _main():
    setup_logger()

    logger.info("Starting the application...")
    source_dir = "/Users/bytedance/Projects/ideaIC-2024.2-sources"
    base_output_file = "ideaIC-2024.2-sources"

    process_directory(source_dir, base_output_file)

    logger.info("Application finished.")


if __name__ == "__main__":
    main()
