# Interactive Modular Translator Tool

## Overview

This tool is a Python-based pipeline designed to run within a Jupyter Notebook environment (specifically optimized for Google Colab). It automates the process of discovering, cloning, and translating entire GitHub repositories from the [ASI Ecosystem](https://www.google.com/search?q=https://github.com/ronniross/asi-ecosystem) into multiple languages using the Google Translate API.

## Features

* **Automated Discovery:** Scrapes the master README to find all related repositories.
* **Interactive UI:** Uses `ipywidgets` to let users select specific repositories and target languages via checkboxes.
* **Smart Translation:** Handles text chunking to respect API character limits and supports retry logic for stability.
* **File Format Support:** Translates code comments and documentation files (e.g., `.md`, `.py`, `.json`, `.txt`).
* **Post-Processing:** Merges translations into single, readable text files and generates detailed reports.
* **Cloud Integration:** Zips the final output and uploads it directly to Google Drive.

---

## Pipeline Workflow

The tool operates in a sequential 9-step pipeline:

### 1. Environment Setup

**Cell 1:** Installs necessary dependencies (`requests`, `deep-translator`, `ipywidgets`, `datasets`) and imports required libraries.

### 2. Repository Discovery

**Cell 2:**

* Fetches the main `README.md` from the `asi-ecosystem` repository.
* Uses Regex to parse the content and extract a unique list of all linked GitHub repositories.

### 3. Repository Selection (Interactive)

**Cell 3:**

* Generates a dynamic UI with checkboxes for every repository found.
* Includes **Select All** and **Deselect All** buttons for batch control.

### 4. Cloning Phase

**Cell 4:**

* Iterates through selected repositories.
* Performs a shallow clone (`git clone --depth 1`) to `cloned_repos/` to save bandwidth and storage.
* Handles errors.

### 5. Language Discovery

**Cell 5:**

* Queries the Google Translate API to retrieve the list of all currently supported languages (133+ languages).

### 6. Language Selection (Interactive)

**Cell 6:**

* Displays a grid of checkboxes for all supported languages.
* Allows the user to select one or multiple target languages for translation.

### 7. Translation Engine (Core Processing)

**Cell 7:**
This is the most computationally intensive step.

* **File Filtering:** Scans repositories for text-based files (extensions include `.txt`, `.md`, `.py`, `.js`, `.json`, etc.).
* **Chunking:** To bypass the API limit (approx. 5000 chars), the tool splits files into chunks of 4500 characters, respecting newline boundaries.
* **Execution:** Translates content chunk-by-chunk and reconstructs the file in the `translations/` directory, maintaining the original folder structure.
* **Reporting:** Generates a `translation_report.json` containing statistics on success and failure rates.

### 8. Merging and formatting

**Cell 8:**

* Consolidates the fragmented file structure.
* For every repository and every language, creates a single `_merged.txt` file (e.g., `asi-protosymbiotic-signal_cs.txt`).
* Adds headers and separators between files for easier reading or ingestion by LLMs.

### 9. Archiving and Export

**Cell 9:**

* Compresses the entire `translations` directory into a timestamped `.zip` file.
* Mounts Google Drive (`/content/drive`).
* Copies the ZIP file to the user's Google Drive root folder for permanent storage.

---

### File System Structure

```text
/content/
├── cloned_repos/               # Raw source code
│   └── [repo_name]/
├── translations/               # Translated outputs
│   └── [repo_name]/
│       └── [lang_code]/        # (e.g., 'es', 'fr')
│           └── [original_structure]
├── merged_translations/        # Consolidated text files
│   └── [repo_name]_[lang_code].txt
└── asi_translations_[date].zip # Final archive

```

---

Ronni Ross
2026
