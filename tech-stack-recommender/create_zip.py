#!/usr/bin/env python3
import os
import zipfile

def create_project_zip(output_filename="tech-stack-recommender.zip"):
    """
    Scans the entire repository structure (including Vercel configuration files,
    API handlers, ML recommender engine, datasets, and frontend source code)
    and packages them into a single, Vercel-ready downloadable ZIP archive.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(base_dir, '..'))

    # Root project directory
    if os.path.exists(os.path.join(parent_dir, 'vercel.json')) or os.path.exists(os.path.join(parent_dir, 'package.json')):
        root_dir = parent_dir
    else:
        root_dir = base_dir

    zip_path = os.path.join(base_dir, output_filename)

    print(f"📦 Packaging project files from root: {root_dir}")
    print(f"⚡ Output ZIP file path: {zip_path}")

    exclude_dirs = {'__pycache__', '.pytest_cache', '.git', '.venv', 'node_modules', 'dist', '.idea', '.vscode'}
    exclude_files = {output_filename, '.DS_Store', 'desktop.ini', 'bun.lock', 'metadata.json'}

    file_count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file in exclude_files or file.endswith('.pyc') or file.endswith('.zip'):
                    continue

                abs_filepath = os.path.join(root, file)
                rel_path = os.path.relpath(abs_filepath, root_dir)

                zipf.write(abs_filepath, rel_path)
                print(f"  + Added: {rel_path}")
                file_count += 1

    print(f"\n✅ Successfully created zip archive with {file_count} files!")
    print(f"📁 Archive ready at: {zip_path}")
    return zip_path

if __name__ == "__main__":
    create_project_zip()
