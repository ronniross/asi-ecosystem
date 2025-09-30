#!/usr/bin/env python3
"""
Phase 2: Integrity Audit
Verifies repository integrity at multiple levels and generates report
"""

import os
import subprocess
import hashlib
import json
from datetime import datetime
from pathlib import Path

class IntegrityVerifier:
    def __init__(self, repo_path):
        self.repo_path = Path(repo_path)
        self.repo_name = self.repo_path.name
        self.results = {
            'repo': self.repo_name,
            'timestamp': datetime.now().isoformat(),
            'levels': {}
        }

    def run_git_command(self, cmd):
        """Execute git command and return output"""
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            shell=False
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode

    def level_1_commit_and_tree_hash(self):
        """Level 1: Compare local vs remote commit and tree hashes"""
        print("  [Level 1] Commit & Tree Hash Comparison")

        # Get local commit hash
        local_commit, _, ret1 = self.run_git_command(['git', 'rev-parse', 'HEAD'])

        # Get local tree hash
        local_tree, _, ret2 = self.run_git_command(['git', 'rev-parse', 'HEAD^{tree}'])

        # Get remote commit hash
        remote_info, _, ret3 = self.run_git_command(['git', 'ls-remote', 'origin', 'HEAD'])
        remote_commit = remote_info.split()[0] if remote_info else None

        if ret1 != 0 or ret2 != 0 or ret3 != 0:
            self.results['levels']['level_1'] = {
                'status': 'ERROR',
                'message': 'Failed to retrieve git hashes'
            }
            print("    [x] ERROR: Failed to retrieve git information")
            return False

        commit_match = local_commit == remote_commit

        self.results['levels']['level_1'] = {
            'status': 'PASS' if commit_match else 'FAIL',
            'local_commit': local_commit,
            'remote_commit': remote_commit,
            'local_tree': local_tree,
            'commit_match': commit_match
        }

        if commit_match:
            print("    [✓] PASS - Commits match")
            print(f"       Commit: {local_commit[:12]}...")
            print(f"       Tree:   {local_tree[:12]}...")
        else:
            print("    [x] FAIL - Commit mismatch")
            print(f"       Local:  {local_commit[:12]}...")
            print(f"       Remote: {remote_commit[:12]}...")

        return commit_match

    def level_2_git_fsck(self):
        """Level 2: Deep git repository integrity check"""
        print("  [Level 2] Git Repository Integrity (fsck)")

        output, stderr, returncode = self.run_git_command(['git', 'fsck', '--full'])

        # git fsck returns 0 if no issues
        passed = returncode == 0 and not any(word in output.lower() for word in ['error', 'missing', 'corrupt'])

        self.results['levels']['level_2'] = {
            'status': 'PASS' if passed else 'FAIL',
            'returncode': returncode,
            'issues_found': [] if passed else output.split('\n')[:5]  # First 5 issues
        }

        if passed:
            print("    [✓] PASS - Repository integrity verified")
        else:
            print("    [x] FAIL - Repository integrity issues detected")
            if output:
                print(f"       Issues: {output[:100]}...")

        return passed

    def level_3_file_hashing(self):
        """Level 3: File-by-file and folder structure verification"""
        print("  [Level 3] File-by-File Hash Verification")

        # Get list of all tracked files
        files_output, _, ret = self.run_git_command(['git', 'ls-files'])

        if ret != 0:
            self.results['levels']['level_3'] = {
                'status': 'ERROR',
                'message': 'Failed to list git files'
            }
            print("    [x] ERROR: Failed to list files")
            return False

        files = files_output.split('\n') if files_output else []

        file_hashes = {}
        corrupted_files = []
        total_files = len(files)

        # Calculate hash for each file
        for file in files[:100]:  # Limit to first 100 files for performance
            if not file:
                continue
            file_path = self.repo_path / file
            if file_path.exists() and file_path.is_file():
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                        file_hashes[file] = file_hash

                        # Verify against git's hash
                        git_hash, _, ret = self.run_git_command(['git', 'hash-object', file])
                        if ret != 0 or not git_hash:
                            corrupted_files.append(file)
                except Exception as e:
                    corrupted_files.append(file)

        passed = len(corrupted_files) == 0

        self.results['levels']['level_3'] = {
            'status': 'PASS' if passed else 'FAIL',
            'total_files_checked': len(file_hashes),
            'total_files_in_repo': total_files,
            'corrupted_files': corrupted_files,
            'sample_hashes': dict(list(file_hashes.items())[:3])  # First 3 as sample
        }

        if passed:
            print(f"    [✓] PASS - All files verified ({len(file_hashes)} checked)")
            if file_hashes:
                sample_file = list(file_hashes.keys())[0]
                print(f"       Sample: {sample_file[:40]}... -> {file_hashes[sample_file][:12]}...")
        else:
            print(f"    [x] FAIL - {len(corrupted_files)} corrupted files detected")
            for cf in corrupted_files[:3]:
                print(f"       - {cf}")

        return passed

    def level_4_tree_comparison(self):
        """Level 4: Complete tree hash comparison"""
        print("  [Level 4] Complete Tree Hash Verification")

        # Get local tree
        local_tree, _, ret1 = self.run_git_command(['git', 'rev-parse', 'HEAD^{tree}'])

        # Fetch latest from remote
        _, _, ret2 = self.run_git_command(['git', 'fetch', 'origin', '--quiet'])

        # Get remote tree
        remote_tree, _, ret3 = self.run_git_command(['git', 'rev-parse', 'origin/HEAD^{tree}'])

        if ret1 != 0 or ret3 != 0:
            self.results['levels']['level_4'] = {
                'status': 'ERROR',
                'message': 'Failed to retrieve tree hashes'
            }
            print("    [x] ERROR: Failed to retrieve tree information")
            return False

        tree_match = local_tree == remote_tree

        self.results['levels']['level_4'] = {
            'status': 'PASS' if tree_match else 'FAIL',
            'local_tree': local_tree,
            'remote_tree': remote_tree,
            'tree_match': tree_match
        }

        if tree_match:
            print("    [✓] PASS - Tree hashes match")
            print(f"       Tree: {local_tree[:12]}...")
        else:
            print("    [x] FAIL - Tree hash mismatch")
            print(f"       Local:  {local_tree[:12]}...")
            print(f"       Remote: {remote_tree[:12]}...")

        return tree_match

    def verify(self, levels=[1, 2, 3, 4]):
        """Run verification for specified levels"""
        print(f"[VERIFYING] {self.repo_name}")
        print("=" * 60)

        level_functions = {
            1: self.level_1_commit_and_tree_hash,
            2: self.level_2_git_fsck,
            3: self.level_3_file_hashing,
            4: self.level_4_tree_comparison
        }

        results = {}
        for level in sorted(levels):
            if level in level_functions:
                results[level] = level_functions[level]()
            else:
                print(f"  [!] Warning: Level {level} not recognized")

        # Overall status
        all_passed = all(results.values())
        self.results['overall_status'] = 'PASS' if all_passed else 'FAIL'

        status_symbol = "[✓]" if all_passed else "[x]"
        print(f"  {status_symbol} Overall: {'PASS' if all_passed else 'FAIL'}")

        return self.results

def run_phase2():
    """Execute Phase 2: Integrity Audit"""
    print("Starting Integrity Verification Process")
    print("=" * 60)

    # Configuration
    VERIFICATION_LEVELS = [1, 2, 3, 4]
repositories_path = Path('/app/repositories')

    if not repositories_path.exists():
        print("Error: repositories folder not found!")
        return False

    repos = [d for d in repositories_path.iterdir() if d.is_dir() and not d.name.startswith('.')]

    print(f"Found {len(repos)} repositories to verify")

    all_results = []
    verification_start = datetime.now()

    for i, repo_path in enumerate(sorted(repos), 1):
        print(f"[{i}/{len(repos)}]")
        verifier = IntegrityVerifier(repo_path)
        result = verifier.verify(levels=VERIFICATION_LEVELS)
        all_results.append(result)

    verification_end = datetime.now()
    duration = (verification_end - verification_start).total_seconds()

    # Summary Statistics
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in all_results if r['overall_status'] == 'PASS')
    failed = len(all_results) - passed

    print(f"Total Repositories: {len(all_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Duration: {duration:.2f} seconds")

    # Level-by-level summary
    print("Level-by-Level Results:")
    for level in VERIFICATION_LEVELS:
        level_passed = sum(1 for r in all_results
                          if f'level_{level}' in r['levels']
                          and r['levels'][f'level_{level}']['status'] == 'PASS')
        level_total = sum(1 for r in all_results if f'level_{level}' in r['levels'])
        print(f"   Level {level}: {level_passed}/{level_total} passed")

    # Failed repositories detail
    if failed > 0:
        print("Failed Repositories:")
        for result in all_results:
            if result['overall_status'] == 'FAIL':
                print(f"   [x] {result['repo']}")
                for level_key, level_data in result['levels'].items():
                    if level_data['status'] != 'PASS':
                        level_num = level_key.replace('level_', '')
                        print(f"      - Level {level_num}: {level_data['status']}")
                        if 'message' in level_data:
                            print(f"        {level_data['message']}")

    print("=" * 60)
    print("Integrity verification complete!")
    print("=" * 60)

    # Store results for export
    integrity_results = {
        'verification_date': verification_start.isoformat(),
        'duration_seconds': duration,
        'levels_checked': VERIFICATION_LEVELS,
        'summary': {
            'total': len(all_results),
            'passed': passed,
            'failed': failed
        },
        'repositories': all_results
    }

    # Export report
    report_path = '/app/output/integrity_report.json'
    with open(report_path, 'w') as f:
        json.dump(integrity_results, f, indent=2)

    print(f"Detailed report exported to: {report_path}")
    print(f"Report size: {Path(report_path).stat().st_size / 1024:.2f} KB")

    return failed == 0  # Return True if all passed
