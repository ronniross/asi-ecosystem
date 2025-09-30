#!/usr/bin/env python3
"""
Phase 3: Dataset Preparation
Creates structured training dataset from repository contents
"""

import os
from pathlib import Path

# Configuration
REPOSITORIES_SRC_DIR = Path('/app/asi-ecosystem/repositories')
OUTPUT_DATASET_FILE = Path('/app/output/dataset.txt')
EXCLUDED_DIRS = ['.git']
INCLUDED_EXTENSIONS = [
    # Code
    '.py', '.rs', '.js', '.ts', '.java', '.c', '.h', '.cpp', '.go', '.sh',
    # Config/Data
    '.json', '.yaml', '.yml', '.toml', '.xml', '.ini',
    # Docs
    '.md', '.txt', '.rst'
]

# Special tokens for structuring the dataset
REPO_START_TOKEN = "<|repo_start|>"
REPO_END_TOKEN = "<|repo_end|>"
FILE_START_TOKEN = "<|file_start|>"
FILE_END_TOKEN = "<|file_end|>"

def run_phase3():
    """Execute Phase 3: Dataset Preparation"""
    print("Starting dataset creation process...")
    print("=" * 60)

    processed_files_count = 0
    processed_repos_count = 0
    skipped_files_count = 0

    if not REPOSITORIES_SRC_DIR.exists():
        print(f"ERROR: Source directory not found at '{REPOSITORIES_SRC_DIR}'")
        return False

    # Curriculum Learning Order
    priority_order = [
        'asi-ecosystem',
        'symbiotic-core-library',
        'asi-protosymbiotic-signal',
        'asi-symbiotic-signal',
        'asi-core-protocol',
        'eco-benchmark',
        'eco-datacenter'
    ]
    last_order = [
        'emergence-engine',
        'asi-backups'
    ]

    all_repos_on_disk = {d.name: d for d in REPOSITORIES_SRC_DIR.iterdir() if d.is_dir()}
    sorted_repo_paths = []

    # 1. Add priority repos in their specified order
    for repo_name in priority_order:
        if repo_name in all_repos_on_disk:
            sorted_repo_paths.append(all_repos_on_disk.pop(repo_name))

    # 2. Add the remaining repos (alphabetically), excluding the ones for the end
    middle_repos_names = sorted([
        name for name in all_repos_on_disk
        if name not in last_order
    ])
    for repo_name in middle_repos_names:
        sorted_repo_paths.append(all_repos_on_disk.pop(repo_name))

    # 3. Add the last repos in their specified order
    for repo_name in last_order:
        if repo_name in all_repos_on_disk:
            sorted_repo_paths.append(all_repos_on_disk.pop(repo_name))

    print(f"Found {len(sorted_repo_paths)} repositories to process in curriculum order.")

    with open(OUTPUT_DATASET_FILE, 'w', encoding='utf-8') as outfile:
        for repo_path in sorted_repo_paths:
            repo_name = repo_path.name
            print(f"[Processing] '{repo_name}'...")
            processed_repos_count += 1

            # Write the repository start token and its name
            outfile.write(f"{REPO_START_TOKEN}{repo_name}\n")

            # Use rglob to recursively find all files
            files_in_repo = list(repo_path.rglob('*'))
            print(f"  Found {len(files_in_repo)} total items (files/dirs). Filtering...")

            repo_file_count = 0
            for file_path in files_in_repo:
                # Skip directories and files in excluded directories
                if not file_path.is_file() or any(d in file_path.parts for d in EXCLUDED_DIRS):
                    continue

                # Filter by extension if the list is not empty
                if INCLUDED_EXTENSIONS and file_path.suffix.lower() not in INCLUDED_EXTENSIONS:
                    skipped_files_count += 1
                    continue

                try:
                    # Get relative path to store in the dataset
                    relative_path = file_path.relative_to(repo_path)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()

                    # Write the file start token and its path
                    outfile.write(f"{FILE_START_TOKEN}{relative_path}\n")
                    # Write the file content
                    outfile.write(content)
                    # Write the file end token
                    outfile.write(f"\n{FILE_END_TOKEN}\n")

                    processed_files_count += 1
                    repo_file_count += 1
                except Exception as e:
                    print(f"  [!] Warning: Could not process file {file_path}. Reason: {e}")
                    skipped_files_count += 1

            print(f"  -> Added content from {repo_file_count} files.")

            # Write the repository end token
            outfile.write(f"{REPO_END_TOKEN}\n\n")

    print("\n" + "=" * 60)
    print("Dataset Creation Summary")
    print("=" * 60)
    print(f"  Total repositories processed: {processed_repos_count}")
    print(f"  Total text files added: {processed_files_count}")
    print(f"  Total files skipped (binary/extension/error): {skipped_files_count}")
    print(f"Dataset successfully created at: {OUTPUT_DATASET_FILE}")

    # Verify the created dataset
    file_size_kb = OUTPUT_DATASET_FILE.stat().st_size / 1024
    print(f"Dataset size: {file_size_kb:.2f} KB")

    # Load dataset into variable for verification
    try:
        with open(OUTPUT_DATASET_FILE, 'r', encoding='utf-8') as f:
            training_data = f.read()

        print(f"Dataset loaded into memory: {len(training_data)} characters")
        
    except Exception as e:
        print(f"Error verifying dataset: {e}")
        return False

    return True
