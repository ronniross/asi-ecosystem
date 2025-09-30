#!/usr/bin/env python3
"""
Phase 1: Ecosystem Cloning
Clones the main ASI ecosystem repository and all component repositories
"""

import os
import subprocess
from pathlib import Path

def run_phase1():
    print("Setting up ASI Ecosystem Integration...")
    
    # Change to app directory
    os.chdir('/app')
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        # Step 1: Clone the main ASI ecosystem repository
        print("Step 1: Cloning the main asi-ecosystem repository...")
        
        # Remove any existing asi-ecosystem directory
        if os.path.exists('asi-ecosystem'):
            print("Removing existing asi-ecosystem directory...")
            subprocess.run(['rm', '-rf', 'asi-ecosystem'], check=True)
        
        # Clone the main repository
        result = subprocess.run([
            'git', 'clone',
            'https://github.com/ronniross/asi-ecosystem.git'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Successfully cloned asi-ecosystem repository")
        else:
            print("Error cloning repository:")
            print(result.stderr)
            return False
        
        # Step 2: Navigate to the directory and check contents
        print("Step 2: Navigating into the directory...")
        os.chdir('/app/asi-ecosystem')
        print(f"Current working directory: {os.getcwd()}")
        
        print("Repository contents:")
        for item in os.listdir('.'):
            print(f"  {item}" if os.path.isdir(item) else f"  {item}")
        
        # Step 3: Check if the script exists and make it executable
        script_path = './scripts/clone_ecosystem.sh'
        print(f"Checking for script at: {script_path}")
        
        if os.path.exists(script_path):
            print("Script found!")
            # Make the script executable
            subprocess.run(['chmod', '+x', script_path], check=True)
            print("Made script executable")
        else:
            print("Script not found. Listing scripts directory:")
            if os.path.exists('scripts'):
                for item in os.listdir('scripts'):
                    print(f"  scripts/{item}")
            else:
                print("  scripts directory does not exist")
            return False
        
        # Step 4: Execute the integration script
        print("Step 3: Running the ecosystem integration script...")
        
        if os.path.exists(script_path):
            try:
                # Run the script and capture output
                result = subprocess.run([script_path],
                                      capture_output=True,
                                      text=True,
                                      cwd='/app/asi-ecosystem')
                
                print("Script output:")
                print(result.stdout)
                
                if result.stderr:
                    print("Script errors/warnings:")
                    print(result.stderr)
                
                if result.returncode == 0:
                    print("Script executed successfully!")
                else:
                    print(f"Script failed with return code: {result.returncode}")
                    return False
                
            except Exception as e:
                print(f"Error executing script: {e}")
                return False
        else:
            print("Cannot execute script - file not found")
            return False
        
        # Step 5: Verify the final result
        print("Step 4: Verifying the final result...")
        
        print(f"Contents of {os.getcwd()}:")
        for item in sorted(os.listdir('.')):
            if os.path.isdir(item):
                print(f"{item}/")
                # If it's the repositories folder, show its contents
                if item == 'repositories':
                    repo_path = os.path.join('.', item)
                    if os.path.exists(repo_path):
                        print(f"  Contents of {item}:")
                        for repo in sorted(os.listdir(repo_path)):
                            print(f"    {repo}/")
            else:
                print(f" {item}")
        
        # Step 6: Summary of cloned repositories
        print("Summary of cloned repositories:")
        repositories_path = './repositories'
        
        if os.path.exists(repositories_path):
            repos = [d for d in os.listdir(repositories_path)
                     if os.path.isdir(os.path.join(repositories_path, d))]
            
            print(f"Total repositories cloned: {len(repos)}")
            for i, repo in enumerate(sorted(repos), 1):
                repo_path = os.path.join(repositories_path, repo)
                # Check if it's a git repository
                git_path = os.path.join(repo_path, '.git')
                status = "Git repo" if os.path.exists(git_path) else "Not a git repo"
                print(f"{i:2d}. {repo:<30} {status}")
        else:
            print("No repositories folder found")
            return False
        
        print("Phase 1 completed successfully!")
        return True
        
    except Exception as e:
        print(f"Phase 1 failed with error: {e}")
        return False
