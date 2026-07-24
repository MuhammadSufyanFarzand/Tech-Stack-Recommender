#!/usr/bin/env python3
import os
import zipfile

def create_project_zip(output_filename="tech-stack-recommender.zip"):
    """
    Scans the tech-stack-recommender directory structure and packages all source code,
    datasets, models, and scripts into a single downloadable ZIP archive.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, output_filename)

    print(f"📦 Packaging project files from: {base_dir}")
    print(f"⚡ Output ZIP file path: {zip_path}")

    exclude_dirs = {'__pycache__', '.pytest_cache', '.git', '.venv', 'node_modules', 'dist', '.idea', '.vscode'}
    exclude_files = {output_filename, '.DS_Store', 'desktop.ini'}

    file_count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file in exclude_files or file.endswith('.pyc') or file.endswith('.zip'):
                    continue

                abs_filepath = os.path.join(root, file)
                rel_path = os.path.relpath(abs_filepath, base_dir)
                archive_name = os.path.join("tech-stack-recommender", rel_path)

                zipf.write(abs_filepath, archive_name)
                print(f"  + Added: {archive_name}")
                file_count += 1

    print(f"\n✅ Successfully created zip archive with {file_count} files!")
    print(f"📁 Archive ready at: {zip_path}")
    return zip_path

if __name__ == "__main__":
    create_project_zip()
