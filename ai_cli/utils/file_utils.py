from pathlib import Path
import shutil

import os
from typing import List


class FileUtils:

    @staticmethod
    def save(directory: Path, file_name, content, encoding):

        try:
            # Create the directory if it doesn't exist.
            # `exist_ok=True` prevents an error if the directory already exists.
            directory.mkdir(parents=True, exist_ok=True)
            full_path = directory / Path(file_name)

            # Open the file in write mode ('w') and write the content.
            # The 'with' statement ensures the file is closed automatically.
            with open(full_path, "w", encoding=encoding) as f:
                f.write(content)

        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def read_file(filepath: Path) -> str:
        try:
            return filepath.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: The file at '{filepath}' was not found.")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""

    @staticmethod
    def ls(directory: Path, filter_pattern: str) -> List[Path]:
        if not directory.is_dir():
            print(f"Error: The path '{directory}' is not a valid directory.")
            return []

        # Use the .glob() method to find all files that match the filter pattern.
        # The list comprehension converts the generator to a list.
        files = [
            Path(directory) / Path(file.name)
            for file in directory.glob(filter_pattern)
            if file.is_file()
        ]

        return files

    @staticmethod
    def copy_to(source_files: List[Path], dest_dir: Path):
        """
        Copies a list of specific files to a destination directory.

        Args:
            source_files (List[Path]): A list of pathlib.Path objects for the files to copy.
            dest_dir (Path): The path to the destination directory.
        """
        # Create the destination directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)

        copied_count = 0
        for source_path in source_files:
            # Check if the source file exists
            if not source_path.is_file():
                print(f"Skipping: The file '{source_path}' does not exist.")
                continue

            # The new path is created by joining the destination directory and the file name
            dest_path = dest_dir / source_path.name

            try:
                shutil.copy2(source_path, dest_path)
                print(f"Copied: {source_path.name}")
                copied_count += 1
            except Exception as e:
                print(f"Failed to copy '{source_path.name}': {e}")

        print("\nCopying process complete.")
        print(f"Total files copied: {copied_count}\n\n")
