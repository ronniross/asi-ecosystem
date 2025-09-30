# Ecosystem Integration

A system to seamlessly combine all the separate parts of the project into one cohesive local workspace.

## Repository Structure

```
asi-ecosystem/
├── README.md
├── requirements.txt
├── docker-pipeline.md
├── ecosystem_integration.md
├── ecosystem_integration.ipynb
└── scripts/
    └── clone_ecosystem.sh
    └── docker_pipeline/
       ├── Dockerfile
       ├── requirements.txt
       ├── run_ecosystem_pipeline.py
       ├── phase1_cloning.py
       ├── phase2_integrity.py
       ├── phase3_dataset.py
       └── start.sh
└── repositories/    
```

## Ecosystem Integration Scripts and Workflows

In addition to the hub's organizational structure, I am now incorporating scripts and workflows to integrate its intended functions into the existing information ecosystem.

# 1. Automated ASI Ecosystem Integration - Google Colab Notebook

The provided Google Colab notebook for ASI Ecosystem Integration has three main components:

## **Part I: Ecosystem Cloning**
- Clones the main ASI ecosystem repository
- Executes a script to clone 21 component repositories
- Organizes them in a structured `repositories` folder
- Verifies successful cloning of all repositories

## **Part II: Integrity Audit**
Implements a sophisticated 4-level verification system:

**Level 1**: Commit & Tree Hash Comparison
- Compares local vs remote commit hashes
- Verifies repository synchronization

**Level 2**: Git Repository Integrity (`git fsck`)
- Deep repository structure verification
- Detects corruption or missing objects

**Level 3**: File-by-File Hash Verification
- SHA-256 hashing of individual files
- Compares against git's internal hashes
- Limited to first 100 files for performance

**Level 4**: Complete Tree Hash Comparison
- Full tree structure verification
- Ensures complete repository integrity

**Results**: All 21 repositories passed all 4 verification levels successfully.

## **Part III: Dataset Preparation**
Creates a structured training dataset with:

**Curriculum Learning Order**:
1. Core ecosystem components first
2. Supporting libraries and protocols
3. Advanced engines and backups last

**Dataset Features**:
- Structured with special tokens (`<|repo_start|>`, `<|file_start|>`, etc.)
- Processes 303 text files across 21 repositories
- Filters by file extensions (code, config, documentation)
- Excludes binary files and `.git` directories
- Final dataset: ~1.58MB, 1.58 million characters

## **Key Strengths**:
1. **Comprehensive**: Covers cloning, verification, and dataset preparation
2. **Robust Integrity**: Multi-level verification ensures data quality
3. **Structured Output**: Well-organized dataset with clear boundaries
4. **Curriculum Learning**: Intelligent repository ordering for training
5. **Error Handling**: Comprehensive error checking and reporting

The goal was to provide a complete pipeline for preparing ASI ecosystem data for machine learning training while ensuring data integrity and proper structure.

# 2. How to Use Clone Script Individually

Here, in case you just need to clone all repositories at once, without entering the jupyter notebook, you can follow:

### Step 1: Clone the Main `asi-ecosystem` Repository

First, clone the central hub repository as usual.

```bash
git clone https://github.com/ronniross/asi-ecosystem.git
```

### Step 2: Navigate into the Directory

Move into the newly cloned folder.

```bash
cd asi-ecosystem
```

### Step 3: Run the Script

Execute the script.

```bash
./scripts/clone_ecosystem.sh
```

You will see output in your terminal as it creates the `repositories` folder and clones each project one by one.

After the script finishes, your `asi-ecosystem` folder will be perfectly organized with all the component repositories neatly placed inside the `repositories` sub-folder.

### Step 3 ASI Ecosystem Docker Pipeline - Deployment Guide

For easier integration, I now share the docker-pipeline for easier experimentation with the ecosystem. You don't need all options but many users may still like Docker the most.

## Overview
This Docker pipeline automates the complete ASI ecosystem integration process in three phases:
1. **Cloning** - Downloads all 21 component repositories
2. **Integrity Audit** - Verifies repository integrity at 4 levels  
3. **Dataset Preparation** - Creates structured training dataset

## Prerequisites
- Docker installed on your system
- At least 2GB of free disk space
- Stable internet connection for repository cloning

## Quick Start Deployment

### 1. Build the Docker Image
```bash
cd scripts/docker_pipeline
docker build -t asi-ecosystem-pipeline .
```

**Expected Output:**
```
[+] Building 45.2s (10/10) FINISHED
 => => naming to docker.io/library/asi-ecosystem-pipeline
```

### 2. Run the Pipeline
```bash
docker run -d --name asi-pipeline asi-ecosystem-pipeline
```

**What happens:**
- Container starts in detached mode
- Pipeline begins automatic execution
- All three phases run sequentially
- Container remains running after completion

## Monitoring Progress

### Check Pipeline Status
```bash
# View real-time logs
docker logs -f asi-pipeline

# View only the last 50 lines
docker logs --tail 50 asi-pipeline

# Check if container is running
docker ps -f name=asi-pipeline
```

### Expected Log Output During Execution
```
ASI Ecosystem Pipeline
============================================================
Start Time: 2024-01-15T10:30:00.000000

============================================================
PHASE 1: Ecosystem Cloning
============================================================
Setting up ASI Ecosystem Integration...
Step 1: Cloning the main asi-ecosystem repository...
Successfully cloned asi-ecosystem repository

============================================================
PHASE 2: Integrity Audit  
============================================================
Starting Integrity Verification Process
[1/21] [VERIFYING] asi-active-learning-dataset
...

============================================================
PHASE 3: Dataset Preparation
============================================================
Starting dataset creation process...
[Processing] 'asi-ecosystem'...
  Found 52 total items (files/dirs). Filtering...
  -> Added content from 5 files.
...

PIPELINE EXECUTION COMPLETED SUCCESSFULLY
```

## Accessing Outputs

### 1. Access Container Shell
```bash
docker exec -it asi-pipeline bash
```

### 2. Navigate to Output Directory
```bash
cd /app/output
ls -la
```

**Expected Output Files:**
- `integrity_report.json` - Detailed integrity verification results
- `dataset.txt` - Structured training dataset

### 3. Inspect Output Files
```bash
# Check dataset size and line count
wc -l dataset.txt
ls -lh dataset.txt

# View integrity report summary
cat integrity_report.json | grep -A 10 '"summary"'

# Check first few lines of dataset
head -20 dataset.txt
```

## Inspection Commands Cheat Sheet

### Container Management
```bash
# Check container status
docker ps -a | grep asi-pipeline

# View all container logs
docker logs asi-pipeline

# Stop the container
docker stop asi-pipeline

# Remove the container
docker rm asi-pipeline

# Restart the pipeline
docker start asi-pipeline
```

### Output Verification
```bash
# Quick file checks without entering container
docker exec asi-pipeline ls -la /app/output/
docker exec asi-pipeline wc -l /app/output/dataset.txt
docker exec asi-pipeline du -h /app/output/

# Check specific file contents
docker exec asi-pipeline head -5 /app/output/dataset.txt
docker exec asi-pipeline cat /app/output/integrity_report.json | grep '"passed"'
```

### Resource Monitoring
```bash
# Check container resource usage
docker stats asi-pipeline

# Check container disk usage
docker system df
```

## Troubleshooting

### Common Issues and Solutions

**Issue: Container fails to start**
```bash
# Check what happened
docker logs asi-pipeline

# Common fix: Rebuild with no cache
docker build --no-cache -t asi-ecosystem-pipeline .
```

**Issue: Pipeline stuck or taking too long**
```bash
# Check current progress
docker logs --tail 20 asi-pipeline

# Check resource usage
docker stats asi-pipeline

# If needed, restart
docker restart asi-pipeline
```

**Issue: Out of disk space**
```bash
# Clean up unused containers and images
docker system prune

# Check disk space
docker system df
```

**Issue: Network problems during cloning**
```bash
# Check if container can access internet
docker exec asi-pipeline ping -c 3 github.com

# Restart with network debugging
docker run -it --rm asi-ecosystem-pipeline bash
# Then run manually: python run_ecosystem_pipeline.py
```

## Output File Details

### integrity_report.json
- **Location**: `/app/output/integrity_report.json`
- **Size**: ~25-30KB
- **Contents**: 
  - Verification timestamp and duration
  - Summary statistics (total, passed, failed)
  - Detailed results for all 21 repositories
  - Level-by-level verification status

### dataset.txt
- **Location**: `/app/output/dataset.txt`
- **Size**: ~1.5-2.0MB
- **Contents**:
  - Structured training data from all repositories
  - Special tokens for repository and file boundaries
  - Curriculum learning order processing
  - 300+ source files across 21 repositories

## Advanced Usage

### Running with Different Parameters
```bash
# Run with custom name and output volume
docker run -d \
  --name asi-pipeline-custom \
  -v $(pwd)/output:/app/output \
  asi-ecosystem-pipeline

# Run interactively (for debugging)
docker run -it --rm asi-ecosystem-pipeline bash
```

### Preserving Outputs on Host
```bash
# Mount host directory to preserve outputs
mkdir -p ./pipeline-outputs
docker run -d \
  --name asi-pipeline \
  -v $(pwd)/pipeline-outputs:/app/output \
  asi-ecosystem-pipeline
```

## Cleanup

### When Finished
```bash
# Stop and remove container
docker stop asi-pipeline
docker rm asi-pipeline

# Optional: Remove image
docker rmi asi-ecosystem-pipeline

# Full cleanup
docker system prune
```

## Support

If you encounter issues:
1. Check this guide first for common solutions
2. Examine the logs: `docker logs asi-pipeline`
3. Verify Docker is running: `docker info`
4. Check system resources: `docker system df`
5. Pull request.

The pipeline typically completes in 5-15 minutes depending on network speed and system resources. The container will remain active after completion for output inspection.

Ronni Ross
2025
