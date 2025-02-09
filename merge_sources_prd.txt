# Merge Sources Requirements Document

## Overview
This document outlines the requirements for the merge_sources.py script, which processes Java and Kotlin source files from IntelliJ IDEA Community Edition and generates markdown documentation.

## File Processing Requirements

1. Source Directory Processing
   - Recursively traverse the source directory
   - Process only .java and .kt files
   - Handle file reading with UTF-8 encoding
   - Skip files that cannot be processed due to errors

2. Content Filtering
   - Remove copyright and license declarations
   - Skip import statements
   - Preserve class declarations and method signatures
   - Remove method bodies while keeping method signatures
   - Maintain class structure and comments

3. Output Format
   - Generate markdown files with .md extension
   - Include introduction text in each file
   - Format file paths as headers using dot notation
   - Use appropriate code block markers (```java or ```kotlin)
   - Maintain proper markdown formatting

4. File Size Management
   - Split output into multiple files when size exceeds limit
   - Default maximum lines per file: 250,000
   - Track line count accurately including newlines
   - Create new files automatically when needed

5. Progress Tracking
   - Print completion messages for each file
   - Show line count for completed files
   - Handle errors gracefully with error messages

6. Buffer Management
   - Buffer content before writing to handle code blocks
   - Ensure code blocks are not split across files
   - Write buffer when complete code blocks are available
   - Clear buffer after successful writes

7. File Naming
   - Use base filename with incremental counter
   - Format: {base_filename}-{counter}.md
   - Maintain consistent naming across split files

8. Error Handling
   - Catch and log file processing errors
   - Continue processing remaining files on error
   - Maintain data integrity during errors
   - Proper file closure in error cases