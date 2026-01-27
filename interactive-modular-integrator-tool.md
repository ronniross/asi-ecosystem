# Interactive Modular Integrator Tool

## Overview

This tool is a Python-based pipeline designed to run within a Jupyter Notebook environment (specifically optimized for Google Colab). It automates the process of discovering, cloning, consolidating, and integrating entire GitHub repositories from the [ASI Ecosystem](https://github.com/ronniross/asi-ecosystem) into unified text files suitable for LLM consumption and analysis.

## Features

---

## Pipeline Workflow

The tool operates in a sequential 9-step pipeline:

### 1. Environment Setup

**Cell 1:** Installs necessary dependencies (`requests`, `ipywidgets`, `datasets`) and imports required libraries including `pathlib`, `json`, `hashlib`, and `datetime`.

### 2. Repository Discovery

**Cell 2:**

* Fetches the main `README.md` from the `asi-ecosystem` repository.
* Uses Regex to parse the content and extract a unique list of all linked GitHub repositories.
* Filters out the main ecosystem repository to avoid duplication.

### 3. Repository Selection (Interactive)

**Cell 3:**

* Generates a dynamic UI with checkboxes for every repository found.
* Includes **Select All** and **Deselect All** buttons for batch control.
* Displays repository names in an organized grid layout.

### 4. Cloning Phase

**Cell 4:**

* Iterates through selected repositories.
* Performs a shallow clone (`git clone --depth 1`) to `cloned_repos/` to save bandwidth and storage.
* Tracks successfully cloned repositories for subsequent processing.
* Handles errors gracefully with informative messages.

### 5. Content Processing

**Cell 5:**

* Defines supported file extensions for text-based content extraction.
* Implements a robust text file reader with UTF-8 encoding and fallback error handling.
* Creates the directory structure for output files (`integrated_content/`).

### 6. Repository Integration (Core Processing)

**Cell 6:**
This is the most computationally intensive step.

* **File Discovery:** Recursively scans each cloned repository for supported file types.
* **Content Extraction:** Reads and processes text files while skipping binary content.
* **Formatting:** Adds clear headers, separators, and metadata for each file.
* **Consolidation:** Creates individual `.txt` files for each repository with all its content integrated.
* **Logging:** Maintains detailed logs of processed files, success rates, and any errors encountered.

### 7. Master Integration File

**Cell 7:**

* Aggregates all individual repository text files into a single master document.
* Adds comprehensive headers with repository names, file counts, and processing timestamps.
* Creates visual separators between repositories for easy navigation.
* Generates a unified file suitable for LLM context windows or training datasets.

### 8. Hash Generation and Reporting

**Cell 8:**

* Computes SHA256 hashes for each repository's integrated content.
* Creates hash files for integrity verification and change detection.
* Generates a comprehensive JSON report including:
  - Processing timestamp
  - Repository metadata
  - File statistics per repository
  - Hash values for verification
  - Processing logs and error reports
* Provides a detailed summary with file counts, total size, and processing statistics.

### 9. Archiving and Export

**Cell 9:**

* Compresses the entire output into a timestamped `.zip` file containing:
  - Individual repository text files
  - Master merged file
  - Integration report (JSON)
  - Hash files for verification
  - Original cloned repositories (raw format)
  - Auto-generated README explaining contents
* Mounts Google Drive (`/content/drive`).
* Copies the ZIP file to the user's Google Drive root folder for permanent storage.
* Displays comprehensive summary of zip contents and upload confirmation.

---

## File System Structure

```text
/content/
├── cloned_repos/                    # Raw source code
│   └── [repo_name]/
├── integrated_content/              # Processed outputs
│   ├── individual_repos/            # Individual repository text files
│   │   └── [repo_name].txt
│   ├── merged/                      # Master integrated file
│   │   └── asi_ecosystem_integrated_[timestamp].txt
│   ├── hashes/                      # SHA256 hash files
│   │   └── [repo_name]_hashes.txt
│   └── reports/                     # Integration reports
│       └── integration_report_[timestamp].json
└── asi_integration_[timestamp].zip  # Final archive
```

---

## Output File Formats

### Individual Repository Files
Each repository is consolidated into a single `.txt` file with:
- Repository header with name and metadata
- File-by-file content with clear demarcation
- File paths and separators for easy navigation
- Complete source code and documentation

### Master Merged File
A comprehensive document containing:
- Table of contents with all repositories
- Sequential integration of all repositories
- Consistent formatting throughout
- Easy-to-parse structure for LLM processing

### Integration Report (JSON)
Detailed metadata including:
```json
{
  "integration_timestamp": "2026-01-27 19:13:40",
  "total_repositories": 2,
  "repositories": [
    {
      "name": "repository-name",
      "files_processed": 15,
      "total_size_bytes": 45632,
      "hash_sha256": "abc123...",
      "files": ["file1.py", "file2.md", ...]
    }
  ],
  "summary": {
    "total_files_processed": 30,
    "total_size_mb": 0.45
  }
}
```

### Hash Files
SHA256 checksums for verification:
```text
abc123def456...  /path/to/file1.py
789ghi012jkl...  /path/to/file2.md
```

---

## Use Cases

* **LLM Training Data:** Prepare curated datasets from multiple repositories
* **Code Analysis:** Consolidate projects for comprehensive review
* **Documentation Generation:** Extract and merge documentation across repositories
* **Knowledge Base Creation:** Build unified knowledge bases from distributed sources
* **Research Archival:** Create time-stamped snapshots of repository collections
* **Content Migration:** Export repository content for alternative platforms

---

### Security & Integrity
- SHA256 hash generation for content verification
- Timestamped outputs for version tracking
- Original repository preservation in archive
- Comprehensive audit trails in reports

---

Ronni Ross  
2026
