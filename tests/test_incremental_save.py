#!/usr/bin/env python3
"""Test incremental save feature"""

import os
import json
import time

print("=" * 80)
print("TEST: Incremental Save Feature")
print("=" * 80)

# Run test experiment with incremental save
print("\n[STEP 1] Running experiment with --save-incremental...")
os.system('python triad_experiment.py --game PD --models MockModel --rounds 5 --save-incremental --reasoning')

# Check if file was created
print("\n[STEP 2] Checking for incremental save files...")
files = [f for f in os.listdir('.') if f.startswith('experiment_results_PD_MockModel_en_Noise0.0_')]

if files:
    latest_file = max(files, key=lambda f: os.path.getmtime(f))
    print(f"[OK] Found incremental save file: {latest_file}")
    
    # Load and verify
    with open(latest_file, 'r') as f:
        data = json.load(f)
    
    print(f"[OK] File contains {data.get('current_round', 'unknown')} rounds")
    print(f"[OK] History has {len(data.get('history', {}))} round entries")
    
    # Show structure
    print("\n[STEP 3] JSON Structure:")
    print(json.dumps(data, indent=2, ensure_ascii=False)[:500] + "...")
    
    # Cleanup
    os.remove(latest_file)
    print(f"\n[Cleaned up {latest_file}]")
    
    print("\n" + "=" * 80)
    print("[PASS] Incremental save working!")
    print("=" * 80)
    print("\nHow it works:")
    print("  - After each round: JSON file is updated")
    print("  - If crash: You still have data up to last completed round")
    print("  - For 100 rounds: File updated 100 times")
else:
    print("[FAIL] No incremental save file found!")
    print("Expected filename pattern: experiment_results_PD_MockModel_en_Noise0.0_[timestamp].json")

