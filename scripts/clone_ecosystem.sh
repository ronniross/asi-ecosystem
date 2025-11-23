#!/bin/bash

# --- clone_ecosystem.sh ---
# This script fetches the latest README from the 'asi-ecosystem' repo,
# extracts all GitHub repository URLs for 'ronniross', and clones them.

# 1. Configuration
CLONE_DIR="repositories"
# We use the RAW URL to get the pure Markdown text, not the GitHub UI HTML.
README_URL="https://raw.githubusercontent.com/ronniross/asi-ecosystem/main/README.md"

# --- Main Execution ---
echo "Starting the ASI Ecosystem cloning process..."

# 2. Create the target directory if it doesn't exist.
if [ -d "$CLONE_DIR" ]; then
    echo "Directory '$CLONE_DIR' already exists."
else
    echo "Creating directory: '$CLONE_DIR'..."
    mkdir "$CLONE_DIR"
    if [ $? -ne 0 ]; then
        echo "Error: Could not create directory '$CLONE_DIR'. Aborting."
        exit 1
    fi
fi

# 3. Change into the cloning directory.
cd "$CLONE_DIR" || exit

# 4. Fetch README content via curl, parse URLs, and clone.
echo "🔎 Fetching latest list from: $README_URL"

# This pipeline does the following:
#   - curl -s: Downloads the raw README file silently from the web.
#   - grep: Finds lines containing the user profile URL.
#   - sed: Extracts the URL located inside Markdown parentheses (e.g., [text](url)).
#   - sort -u: Ensures unique URLs only.
curl -s "$README_URL" | \
grep 'https://github.com/ronniross/' | \
sed -n 's/.*(\(https:\/\/github\.com\/ronniross\/[a-zA-Z0-9_-]*\)).*/\1/p' | \
sort -u | \
while read repo_url; do
    if [ -n "$repo_url" ]; then
        # Extract the folder name (e.g., 'my-repo' from the URL) to check if it exists
        dir_name=$(basename "$repo_url")

        if [ -d "$dir_name" ]; then
            echo " Skipping $dir_name (already exists)."
        else
            echo " Cloning $repo_url..."
            git clone "$repo_url"
        fi
    fi
done

echo "-------------------------------------------------------"
echo "All repositories have been processed in '$CLONE_DIR'."
echo "ASI Ecosystem clone setup complete!"
