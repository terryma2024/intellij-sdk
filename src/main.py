from directory_processor import process_directory


def main():
    source_dir = "/Users/bytedance/Projects/ideaIC-2024.2-sources"
    base_output_file = "ideaIC-2024.2-sources"

    process_directory(source_dir, base_output_file)


if __name__ == "__main__":
    main()
