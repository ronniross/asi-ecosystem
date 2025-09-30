#!/usr/bin/env python3
"""
Main orchestrator for ASI Ecosystem Pipeline
Executes the three-phase workflow: Cloning → Integrity Audit → Dataset Preparation
"""

import os
import sys
import time
from datetime import datetime

def main():
    print("ASI Ecosystem Pipeline")
    print("=" * 60)
    print(f"Start Time: {datetime.now().isoformat()}")
    print("=" * 60)
    
    # Create output directory
    os.makedirs('/app/output', exist_ok=True)
    
    try:
        # Phase 1: Ecosystem Cloning
        print("\n" + "=" * 60)
        print("PHASE 1: Ecosystem Cloning")
        print("=" * 60)
        from phase1_cloning import run_phase1
        phase1_success = run_phase1()
        
        if not phase1_success:
            print("Phase 1 failed. Stopping pipeline.")
            return False
        
        # Phase 2: Integrity Audit
        print("\n" + "=" * 60)
        print("PHASE 2: Integrity Audit")
        print("=" * 60)
        from phase2_integrity import run_phase2
        phase2_success = run_phase2()
        
        if not phase2_success:
            print("Phase 2 failed. Stopping pipeline.")
            return False
        
        # Phase 3: Dataset Preparation
        print("\n" + "=" * 60)
        print("PHASE 3: Dataset Preparation")
        print("=" * 60)
        from phase3_dataset import run_phase3
        phase3_success = run_phase3()
        
        if not phase3_success:
            print("Phase 3 failed. Stopping pipeline.")
            return False
        
        # Pipeline completed successfully
        print("\n" + "=" * 60)
        print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print(f"End Time: {datetime.now().isoformat()}")
        print("\nOutputs available in /app/output/")
        print(" - integrity_report.json")
        print(" - dataset.txt")
        
        return True
        
    except Exception as e:
        print(f"Pipeline execution failed with error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
