#!/bin/bash

# --- clone_ecosystem.sh ---
# This script extracts all GitHub repository URLs for the user 'ronniross' and clones each one into a 'repositories' subdirectory.

# Set the name for the directory where repos will be cloned.
CLONE_DIR="repositories"

# --- Main Execution ---
echo "Starting the ASI Ecosystem cloning process..."

# 1. Create the target directory if it doesn't exist.
if [ -d "$CLONE_DIR" ]; then
    echo " Directory '$CLONE_DIR' already exists. Skipping creation."
else
    echo " Creating directory: '$CLONE_DIR'..."
    mkdir "$CLONE_DIR"
    if [ $? -ne 0 ]; then
        echo " Error: Could not create directory '$CLONE_DIR'. Aborting."
        exit 1
    fi
fi

# 2. Change into the cloning directory.
cd "$CLONE_DIR"

# 3. Parse README.md from the parent directory, find unique URLs, and clone them.
echo "🔎 Finding repositories in README.md..."

# This command chain does the following:
#   - grep: Finds all lines in the parent directory's README containing the base URL.
#   - sed:  Extracts just the full HTTPS URL from the Markdown link format.
#   - sort -u: Ensures each repository is only cloned once, even if duplicated in the README.
grep 'https://github.com/ronniross/' ../README.md | \
sed -n 's/.*(\(https:\/\/github\.com\/ronniross\/[a-zA-Z0-9_-]*\)).*/\1/p' | \
sort -u | \
while read repo_url; do
    if [ -n "$repo_url" ]; then
        echo " Cloning $repo_url..."
        git clone "$repo_url"
    fi
done

echo "All repositories have been cloned into the '$CLONE_DIR' directory."
echo "ASI Ecosystem clone setup complete!"
