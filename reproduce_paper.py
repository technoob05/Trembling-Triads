"""
REPRODUCTION SCRIPT FOR PROJECT TRIAD
======================================
One-command reproduction of all experiments and analysis for NeurIPS 2026 submission.

Usage:
    python reproduce_paper.py --mode all          # Run everything
    python reproduce_paper.py --mode experiments  # Run experiments only
    python reproduce_paper.py --mode analysis     # Run analysis only  
    python reproduce_paper.py --mode figures      # Generate figures only

Author: Project Triad Research Team
Date: January 28, 2026
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def check_environment():
    """Verify Python version and key dependencies."""
    print("=" * 60)
    print("  ENVIRONMENT CHECK")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 10):
        print(f"❌ Python 3.10+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check key packages
    required = ['numpy', 'pandas', 'matplotlib', 'seaborn']
    missing = []
    
    for pkg in required:
        try:
            __import__(pkg)
            print(f"✅ {pkg} installed")
        except ImportError:
            missing.append(pkg)
            print(f"❌ {pkg} missing")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    return True


def run_experiments():
    """Run all experiments (IPD, PGG, VD) with noise variations."""
    print("\n" + "=" * 60)
    print("  RUNNING EXPERIMENTS")
    print("=" * 60)
    
    experiments = [
        # Prisoner's Dilemma with noise variations
        ["python", "triad_experiment.py", "--game", "PD", "--noise", "0.0", "--lang", "en"],
        ["python", "triad_experiment.py", "--game", "PD", "--noise", "0.05", "--lang", "en"],
        ["python", "triad_experiment.py", "--game", "PD", "--noise", "0.10", "--lang", "en"],
        
        # Public Goods Game
        ["python", "triad_experiment.py", "--game", "PGG", "--noise", "0.0", "--lang", "en"],
        ["python", "triad_experiment.py", "--game", "PGG", "--noise", "0.05", "--lang", "en"],
        
        # Volunteer's Dilemma
        ["python", "triad_experiment.py", "--game", "VD", "--noise", "0.0", "--lang", "en"],
    ]
    
    for i, cmd in enumerate(experiments, 1):
        print(f"\n[{i}/{len(experiments)}] Running: {' '.join(cmd[2:])}")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✅ Completed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed with error:\n{e.stderr}")
            return False
    
    return True


def run_analysis():
    """Run comprehensive analysis on experimental data."""
    print("\n" + "=" * 60)
    print("  RUNNING ANALYSIS")
    print("=" * 60)
    
    print("\n📊 Analyzing experimental results...")
    try:
        result = subprocess.run(
            ["python", "complete_analysis.py"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Analysis completed")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Analysis failed:\n{e.stderr}")
        return False
    
    return True


def generate_figures():
    """Generate all publication-quality figures."""
    print("\n" + "=" * 60)
    print("  GENERATING FIGURES")
    print("=" * 60)
    
    print("\n📈 Creating visualization suite...")
    try:
        result = subprocess.run(
            ["python", "Output_Exp/generate_figures.py"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Figures generated")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Figure generation failed:\n{e.stderr}")
        return False
    
    # Check if figures were created
    figures_dir = Path("Output_Exp/figures")
    if figures_dir.exists():
        figures = list(figures_dir.glob("*.png"))
        print(f"✅ Generated {len(figures)} figures in Output_Exp/figures/")
    
    return True


def verify_output():
    """Verify all expected output files exist."""
    print("\n" + "=" * 60)
    print("  VERIFICATION")
    print("=" * 60)
    
    expected_files = [
        "Output_Exp/COMPREHENSIVE_ANALYSIS.md",
        "Output_Exp/EXECUTIVE_SUMMARY.md",
        "Output_Exp/figures/Figure1_Cooperation_vs_Noise.png",
        "Output_Exp/figures/Figure2_Agent_Behavior.png",
        "Output_Exp/figures/Figure3_Shapley_Heatmap.png",
        "Output_Exp/figures/Figure4_Language_Comparison.png",
        "Output_Exp/figures/Figure5_Trembling_Robustness.png",
    ]
    
    all_exist = True
    for file_path in expected_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist


def main():
    parser = argparse.ArgumentParser(
        description="Reproduce all experiments and analysis for PROJECT TRIAD"
    )
    parser.add_argument(
        "--mode",
        choices=["all", "experiments", "analysis", "figures"],
        default="all",
        help="Which component to run (default: all)"
    )
    parser.add_argument(
        "--skip-check",
        action="store_true",
        help="Skip environment verification (not recommended)"
    )
    
    args = parser.parse_args()
    
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "PROJECT TRIAD REPRODUCTION SCRIPT" + " " * 15 + "║")
    print("║" + " " * 12 + "NeurIPS 2026 Submission Package" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Environment check
    if not args.skip_check:
        if not check_environment():
            print("\n⚠️  Environment check failed. Fix issues before proceeding.")
            return 1
    
    # Execute requested mode
    success = True
    
    if args.mode in ["all", "experiments"]:
        success = success and run_experiments()
    
    if args.mode in ["all", "analysis"]:
        success = success and run_analysis()
    
    if args.mode in ["all", "figures"]:
        success = success and generate_figures()
    
    # Verify output
    if args.mode == "all":
        success = success and verify_output()
    
    # Final summary
    print("\n" + "=" * 60)
    if success:
        print("  ✅ REPRODUCTION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\n📁 Output location: Output_Exp/")
        print("📊 Main analysis: Output_Exp/COMPREHENSIVE_ANALYSIS.md")
        print("📈 Figures: Output_Exp/figures/")
        return 0
    else:
        print("  ❌ REPRODUCTION FAILED")
        print("=" * 60)
        print("\nCheck error messages above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
