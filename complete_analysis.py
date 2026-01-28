#!/usr/bin/env python3
"""
COMPLETE ANALYSIS: Trembling Triads
Inspired by "Nicer than Human" paper - Comprehensive behavioral analysis

This script performs end-to-end analysis including:
- Behavioral dimensions (cooperation, forgiveness, retaliation)
- Strategic pattern recognition (TFT, GRIM, Always Defect)
- Reasoning semantic analysis
- Meta-prompt validation
- Publication-ready visualizations
"""

import json
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter
import re
from scipy import stats
import os

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
OUTPUT_DIR = 'Output_Exp'

print("="*80)
print("COMPREHENSIVE ANALYSIS: TREMBLING TRIADS")
print("Inspired by 'Nicer than Human' (ICWSM 2025)")
print("="*80)

# =============================================================================
# PART 1: DATA LOADING & PREPROCESSING
# =============================================================================

def load_all_data(data_dir='Output_Exp'):
    """Load all JSON experiment results"""
    print("\n[PART 1] DATA LOADING & PREPROCESSING")
    print("-"*80)
    
    pattern = os.path.join(data_dir, 'experiment_results_*.json')
    files = glob.glob(pattern)
    
    print(f"Found {len(files)} result files")
    
    all_experiments = {}
    all_rounds = []
    
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for exp_name, exp_data in data.items():
            if 'ERROR' in exp_name:
                continue
            
            # Parse metadata
            parts = exp_name.split('_')
            game_type = parts[0] if parts else 'Unknown'
            
            # Extract noise
            noise = 0.0
            if 'Noise' in exp_name:
                try:
                    noise = float(exp_name.split('Noise')[1].split('_')[0])
                except:
                    pass
            
            # Extract language
            lang = 'en'
            if '_vn_' in exp_name or '_vn' in exp_name:
                lang = 'vn'
            
            history = exp_data.get('history', {})
            
            # Flatten to round-level data
            for round_key in sorted(history.keys(), key=lambda k: int(k.split('_')[1])):
                round_num = int(round_key.split('_')[1])
                round_data = history[round_key]
                
                for agent_data in round_data:
                    all_rounds.append({
                        'experiment': exp_name,
                        'game': game_type,
                        'noise': noise,
                        'language': lang,
                        'round': round_num,
                        'agent': agent_data['agent'],
                        'strategy': agent_data.get('strategy', 'Unknown'),
                        'intended_strategy': agent_data.get('intended_strategy', 'Unknown'),
                        'is_noise': agent_data.get('is_noise', False),
                        'score': agent_data.get('score', 0),
                        'reasoning': agent_data.get('reasoning', ''),
                        'meta_prompt': agent_data.get('meta_prompt_validation', {})
                    })
            
            all_experiments[exp_name] = {
                'data': exp_data,
                'game': game_type,
                'noise': noise,
                'language': lang,
                'rounds': len(history)
            }
    
    df = pd.DataFrame(all_rounds)
    
    print(f"\nLoaded {len(all_experiments)} experiments")
    print(f"Total rounds: {len(df['round'].unique())}")
    print(f"Total actions: {len(df)}")
    print(f"Games: {df['game'].unique()}")
    print(f"Languages: {df['language'].unique()}")
    print(f"Noise levels: {sorted(df['noise'].unique())}")
    
    print("\nDataFrame shape:", df.shape)
    print("\nSample:")
    print(df.head(3).to_string())
    
    return df, all_experiments

# =============================================================================
# PART 2: BEHAVIORAL DIMENSIONS (from "Nicer than Human")
# =============================================================================

def calculate_behavioral_dimensions(df):
    """
    Calculate behavioral dimensions as defined in 'Nicer than Human':
    - Cooperation Rate
    - Forgiveness (cooperate after opponent defects)
    - Retaliation (defect after opponent defects)
    - Niceness (first move cooperation)
    """
    print("\n[PART 2] BEHAVIORAL DIMENSIONS ANALYSIS")
    print("-"*80)
    
    results = []
    
    for exp_name in df['experiment'].unique():
        exp_df = df[df['experiment'] == exp_name]
        
        for agent_name in exp_df['agent'].unique():
            agent_df = exp_df[exp_df['agent'] == agent_name].sort_values('round')
            
            if len(agent_df) == 0:
                continue
            
            # Calculate dimensions
            total_actions = len(agent_df)
            cooperations = (agent_df['strategy'] == 'Cooperate').sum()
            coop_rate = cooperations / total_actions
            
            # First move
            first_move = agent_df.iloc[0]['strategy'] if len(agent_df) > 0 else 'Unknown'
            niceness = 1 if first_move == 'Cooperate' else 0
            
            # Forgiveness & Retaliation (need opponent history - simplified)
            # For triadic game, we'll track response to ANY defection
            forgiveness_count = 0
            retaliation_count = 0
            opportunities_forgive = 0
            opportunities_retaliate = 0
            
            for idx, row in agent_df.iterrows():
                if row['round'] <= 1:
                    continue
                
                # Get previous round for ALL agents
                prev_round = row['round'] - 1
                prev_round_df = exp_df[exp_df['round'] == prev_round]
                
                # Did ANY opponent defect last round?
                opponents_defected = (prev_round_df[prev_round_df['agent'] != agent_name]['strategy'] == 'Defect').any()
                opponents_cooperated = (prev_round_df[prev_round_df['agent'] != agent_name]['strategy'] == 'Cooperate').any()
                
                if opponents_defected:
                    opportunities_forgive += 1
                    if row['strategy'] == 'Cooperate':
                        forgiveness_count += 1
                    else:
                        retaliation_count += 1
                        opportunities_retaliate += 1
            
            forgiveness = forgiveness_count / opportunities_forgive if opportunities_forgive > 0 else np.nan
            retaliation = retaliation_count / opportunities_retaliate if opportunities_retaliate > 0 else np.nan
            
            results.append({
                'Experiment': exp_name,
                'Agent': agent_name,
                'Cooperation Rate': coop_rate,
                'Niceness': niceness,
                'Forgiveness': forgiveness,
                'Retaliation': retaliation,
                'Total Actions': total_actions
            })
    
    behavior_df = pd.DataFrame(results)
    
    print("\nBehavioral Dimensions Summary:")
    print(behavior_df.groupby('Agent')[['Cooperation Rate', 'Niceness', 'Forgiveness', 'Retaliation']].mean().to_string())
    
    return behavior_df

# =============================================================================
# PART 3: STRATEGIC PATTERN RECOGNITION
# =============================================================================

def detect_strategy_type(agent_actions):
    """
    Detect strategy type based on action sequence.
    Strategies from "Nicer than Human": TFT, GRIM, Always Cooperate, Always Defect, etc.
    """
    if len(agent_actions) < 3:
        return "Insufficient Data"
    
    strategies = agent_actions['strategy'].values
    
    # Always Cooperate
    if all(s == 'Cooperate' for s in strategies):
        return "Always Cooperate (AC)"
    
    # Always Defect
    if all(s == 'Defect' for s in strategies):
        return "Always Defect (AD)"
    
    # Mostly patterns
    coop_rate = (strategies == 'Cooperate').mean()
    if coop_rate > 0.8:
        return "Mostly Cooperate"
    elif coop_rate < 0.2:
        return "Mostly Defect"
    
    # Check for Tit-for-Tat pattern (simplified - actual TFT detection complex in triadic)
    # TFT: mirrors opponent's previous move
    # In triadic game, this is approximate
    
    return "Mixed Strategy"

def analyze_strategic_patterns(df):
    """Identify strategy types for each agent"""
    print("\n[PART 3] STRATEGIC PATTERN RECOGNITION")
    print("-"*80)
    
    patterns = []
    
    for exp_name in df['experiment'].unique():
        exp_df = df[df['experiment'] == exp_name]
        
        for agent_name in exp_df['agent'].unique():
            agent_df = exp_df[exp_df['agent'] == agent_name].sort_values('round')
            strategy_type = detect_strategy_type(agent_df)
            
            patterns.append({
                'Experiment': exp_name[:40],
                'Agent': agent_name,
                'Strategy Type': strategy_type,
                'Cooperation Rate': (agent_df['strategy'] == 'Cooperate').mean()
            })
    
    pattern_df = pd.DataFrame(patterns)
    
    print("\nStrategy Distribution:")
    print(pattern_df['Strategy Type'].value_counts().to_string())
    
    print("\n\nBy Agent:")
    print(pattern_df.groupby('Agent')['Strategy Type'].value_counts().to_string())
    
    return pattern_df

# =============================================================================
# PART 4: REASONING ANALYSIS
# =============================================================================

def analyze_reasoning_semantics(df):
    """Deep analysis of reasoning text"""
    print("\n[PART 4] REASONING SEMANTIC ANALYSIS")
    print("-"*80)
    
    # Extract reasoning by strategy
    coop_reasoning = df[df['strategy'] == 'Cooperate']['reasoning'].dropna()
    defect_reasoning = df[df['strategy'] == 'Defect']['reasoning'].dropna()
    
    # Remove non-meaningful reasoning
    coop_reasoning = coop_reasoning[coop_reasoning.str.len() > 20]
    defect_reasoning = defect_reasoning[defect_reasoning.str.len() > 20]
    
    print(f"\nReasoning Samples:")
    print(f"  Cooperate: {len(coop_reasoning)} samples")
    print(f"  Defect: {len(defect_reasoning)} samples")
    
    # Keyword analysis
    keywords = {
        'trust': ['trust', 'reliable', 'trustworthy'],
        'long-term': ['long-term', 'future', 'long run'],
        'mutual': ['mutual', 'both', 'together'],
        'risk': ['risk', 'vulnerable', 'exploited'],
        'maximize': ['maximize', 'maximum', 'optimal'],
        'retaliation': ['retaliate', 'punish', 'revenge', 'payback'],
        'protection': ['protect', 'avoid', 'prevent'],
        'reciprocity': ['reciprocate', 'mirror', 'tit-for-tat']
    }
    
    def count_keywords(text_series, keyword_dict):
        counts = {cat: 0 for cat in keyword_dict}
        for text in text_series:
            text_lower = text.lower()
            for category, keywords in keyword_dict.items():
                if any(kw in text_lower for kw in keywords):
                    counts[category] += 1
        return counts
    
    coop_keywords = count_keywords(coop_reasoning, keywords)
    defect_keywords = count_keywords(defect_reasoning, keywords)
    
    print("\nKeyword Frequency in COOPERATE reasoning:")
    for cat, count in sorted(coop_keywords.items(), key=lambda x: -x[1])[:5]:
        pct = count / len(coop_reasoning) * 100
        print(f"  {cat}: {count} ({pct:.1f}%)")
    
    print("\nKeyword Frequency in DEFECT reasoning:")
    for cat, count in sorted(defect_keywords.items(), key=lambda x: -x[1])[:5]:
        pct = count / len(defect_reasoning) * 100
        print(f"  {cat}: {count} ({pct:.1f}%)")
    
    # Sample reasoning
    print("\n\nSample COOPERATE Reasoning (top 3):")
    for i, reason in enumerate(coop_reasoning.head(3), 1):
        print(f"\n  [{i}] {reason[:150]}...")
    
    print("\n\nSample DEFECT Reasoning (top 3):")
    for i, reason in enumerate(defect_reasoning.head(3), 1):
        print(f"\n  [{i}] {reason[:150]}...")
    
    return {
        'cooperate': coop_reasoning,
        'defect': defect_reasoning,
        'keywords': {'cooperate': coop_keywords, 'defect': defect_keywords}
    }

# =============================================================================
# PART 5: META-PROMPT VALIDATION ANALYSIS
# =============================================================================

def analyze_meta_prompts(df):
    """Analyze meta-prompt validation responses"""
    print("\n[PART 5] META-PROMPT VALIDATION ANALYSIS")
    print("-"*80)
    
    # Filter rows with meta-prompts
    meta_df = df[df['meta_prompt'].apply(lambda x: bool(x))].copy()
    
    if len(meta_df) == 0:
        print("No meta-prompt data found")
        return None
    
    print(f"\nMeta-prompt samples: {len(meta_df)}")
    print(f"Rounds with validation: {meta_df['round'].unique()}")
    
    # Check comprehension quality
    def check_payoff_understanding(text):
        """Check if agent understands payoff structure"""
        if not text or len(text) < 10:
            return 0
        text_lower = text.lower()
        # Look for key concepts
        score = 0
        if any(word in text_lower for word in ['lower', 'decrease', 'less', 'sucker']):
            score += 1
        if any(word in text_lower for word in ['defect', 'betray']):
            score += 1
        return score / 2  # 0 to 1
    
    comprehension_scores = []
    
    for _, row in meta_df.iterrows():
        meta = row['meta_prompt']
        if isinstance(meta, dict):
            payoff_understanding = meta.get('payoff_understanding', '')
            score = check_payoff_understanding(payoff_understanding)
            comprehension_scores.append(score)
    
    avg_comprehension = np.mean(comprehension_scores) if comprehension_scores else 0
    
    print(f"\nComprehension Quality Score: {avg_comprehension:.2f} (0-1 scale)")
    
    # Show examples
    print("\nSample Meta-Prompt Responses:")
    for idx, row in meta_df.head(2).iterrows():
        meta = row['meta_prompt']
        if isinstance(meta, dict):
            print(f"\n  Agent: {row['agent']}, Round: {row['round']}")
            print(f"    Payoff: {meta.get('payoff_understanding', 'N/A')[:80]}...")
            print(f"    Strategy: {meta.get('strategy_understanding', 'N/A')[:80]}...")
    
    return meta_df

# =============================================================================
# PART 6: VISUALIZATIONS (Publication-Ready)
# =============================================================================

def create_comprehensive_visualizations(df, behavior_df, reasoning_data):
    """Generate all figures for paper"""
    print("\n[PART 6] GENERATING PUBLICATION-READY VISUALIZATIONS")
    print("-"*80)
    
    # Figure 1: Cooperation Rate by Agent and Noise
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # By agent
    agent_coop = df.groupby('agent')['strategy'].apply(lambda x: (x == 'Cooperate').mean() * 100)
    axes[0].bar(agent_coop.index, agent_coop.values, color=['#3498db', '#e74c3c', '#2ecc71'], alpha=0.7)
    axes[0].set_ylabel('Cooperation Rate (%)')
    axes[0].set_title('Cooperation Rate by Agent\n(Personality Effect)', fontweight='bold')
    axes[0].set_ylim([0, 105])
    
    for i, v in enumerate(agent_coop.values):
        axes[0].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # By noise
    noise_coop = df.groupby('noise')['strategy'].apply(lambda x: (x == 'Cooperate').mean() * 100)
    axes[1].plot(noise_coop.index * 100, noise_coop.values, marker='o', linewidth=3, markersize=10, color='#e74c3c')
    axes[1].set_xlabel('Noise Level ε (%)')
    axes[1].set_ylabel('Cooperation Rate (%)')
    axes[1].set_title('Cooperation vs. Noise\n(Trembling Hand Robustness)', fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim([0, 50])
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig1_behavioral_dimensions.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: fig1_behavioral_dimensions.png")
    plt.close()
    
    # Figure 2: Round-by-Round Trajectory (ALL agents)
    fig, ax = plt.subplots(figsize=(16, 8))
    
    for exp_name in df['experiment'].unique():
        exp_df = df[df['experiment'] == exp_name]
        noise = exp_df['noise'].iloc[0]
        
        round_coop = exp_df.groupby('round')['strategy'].apply(lambda x: (x == 'Cooperate').mean() * 100)
        
        ax.plot(round_coop.index, round_coop.values, alpha=0.6, linewidth=1.5, 
               label=f"ε = {noise:.0%}")
    
    ax.set_xlabel('Round Number', fontsize=14)
    ax.set_ylabel('Cooperation Rate (%)', fontsize=14)
    ax.set_title('Figure 2: Cooperation Evolution Over Time (All Experiments)', fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 80])
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig2_temporal_dynamics.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: fig2_temporal_dynamics.png")
    plt.close()
    
    # Figure 3: Behavioral Dimensions Heatmap
    if behavior_df is not None and len(behavior_df) > 0:
        fig, ax = plt.subplots(figsize=(10, 8))
        
        pivot = behavior_df.groupby('Agent')[['Cooperation Rate', 'Niceness', 'Forgiveness', 'Retaliation']].mean()
        sns.heatmap(pivot.T, annot=True, fmt='.2f', cmap='RdYlGn', vmin=0, vmax=1, ax=ax, cbar_kws={'label': 'Score (0-1)'})
        ax.set_title('Figure 3: Behavioral Dimensions Heatmap\n(Inspired by "Nicer than Human")', fontsize=14, fontweight='bold')
        ax.set_xlabel('Agent')
        ax.set_ylabel('Behavioral Dimension')
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'fig3_behavioral_heatmap.png'), dpi=300, bbox_inches='tight')
        print(f"Saved: fig3_behavioral_heatmap.png")
        plt.close()
    
    # Figure 4: Reasoning Keyword Analysis
    if reasoning_data:
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Cooperate keywords
        coop_kw = reasoning_data['keywords']['cooperate']
        sorted_coop = sorted(coop_kw.items(), key=lambda x: -x[1])[:8]
        axes[0].barh([k for k, v in sorted_coop], [v for k, v in sorted_coop], color='#2ecc71', alpha=0.7)
        axes[0].set_xlabel('Frequency')
        axes[0].set_title('COOPERATE Reasoning - Key Themes', fontweight='bold')
        axes[0].invert_yaxis()
        
        # Defect keywords
        defect_kw = reasoning_data['keywords']['defect']
        sorted_defect = sorted(defect_kw.items(), key=lambda x: -x[1])[:8]
        axes[1].barh([k for k, v in sorted_defect], [v for k, v in sorted_defect], color='#e74c3c', alpha=0.7)
        axes[1].set_xlabel('Frequency')
        axes[1].set_title('DEFECT Reasoning - Key Themes', fontweight='bold')
        axes[1].invert_yaxis()
        
        plt.suptitle('Figure 4: Reasoning Semantic Analysis', fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'fig4_reasoning_keywords.png'), dpi=300, bbox_inches='tight')
        print(f"Saved: fig4_reasoning_keywords.png")
        plt.close()
    
    # Figure 5: Agent Comparison (Multi-panel)
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    # Panel A: Cooperation over time by agent
    ax1 = fig.add_subplot(gs[0, :])
    for agent in df['agent'].unique():
        agent_df = df[df['agent'] == agent]
        round_coop = agent_df.groupby('round')['strategy'].apply(lambda x: (x == 'Cooperate').mean() * 100)
        ax1.plot(round_coop.index, round_coop.values, linewidth=2, marker='o', markersize=3, 
                label=agent, alpha=0.8)
    
    ax1.set_xlabel('Round Number')
    ax1.set_ylabel('Cooperation Rate (%)')
    ax1.set_title('Panel A: Cooperation Trajectory by Agent', fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Panel B: Noise impact by agent
    ax2 = fig.add_subplot(gs[1, 0])
    for agent in df['agent'].unique():
        agent_df = df[df['agent'] == agent]
        noise_coop = agent_df.groupby('noise')['strategy'].apply(lambda x: (x == 'Cooperate').mean() * 100)
        ax2.plot(noise_coop.index * 100, noise_coop.values, marker='o', linewidth=2, label=agent)
    
    ax2.set_xlabel('Noise Level ε (%)')
    ax2.set_ylabel('Cooperation Rate (%)')
    ax2.set_title('Panel B: Noise Sensitivity by Agent', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Panel C: Strategy distribution
    ax3 = fig.add_subplot(gs[1, 1])
    strategy_counts = df.groupby(['agent', 'strategy']).size().unstack(fill_value=0)
    strategy_counts.plot(kind='bar', ax=ax3, color=['#2ecc71', '#e74c3c'], alpha=0.7)
    ax3.set_ylabel('Action Count')
    ax3.set_title('Panel C: Strategy Distribution', fontweight='bold')
    ax3.legend(title='Strategy')
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0)
    
    plt.suptitle('Figure 5: Comprehensive Agent Comparison', fontsize=16, fontweight='bold')
    plt.savefig(os.path.join(OUTPUT_DIR, 'fig5_agent_comparison.png'), dpi=300, bbox_inches='tight')
    print(f"Saved: fig5_agent_comparison.png")
    plt.close()
    
    print("\nAll visualizations generated!")

# =============================================================================
# PART 7: STATISTICAL TESTS & PAPER TABLES
# =============================================================================

def generate_statistical_summary(df, behavior_df):
    """Generate statistical tests and tables for paper"""
    print("\n[PART 7] STATISTICAL ANALYSIS & PAPER TABLES")
    print("-"*80)
    
    # Table 1: Overall Summary Statistics
    print("\n### TABLE 1: Summary Statistics")
    print("-"*80)
    summary_stats = {
        'Total Experiments': df['experiment'].nunique(),
        'Total Rounds': df['round'].max(),
        'Total Actions': len(df),
        'Overall Cooperation Rate': f"{(df['strategy'] == 'Cooperate').mean():.1%}",
        'Noise Events': df['is_noise'].sum(),
        'Reasoning Samples': df['reasoning'].apply(lambda x: len(x) > 20 if isinstance(x, str) else False).sum()
    }
    
    for key, val in summary_stats.items():
        print(f"{key:.<40} {val}")
    
    # Table 2: Behavioral Dimensions by Agent
    if behavior_df is not None:
        print("\n### TABLE 2: Behavioral Dimensions by Agent")
        print("-"*80)
        agent_summary = behavior_df.groupby('Agent')[['Cooperation Rate', 'Niceness', 'Forgiveness', 'Retaliation']].agg(['mean', 'std'])
        print(agent_summary.to_string())
    
    # Table 3: Noise Impact
    print("\n### TABLE 3: Cooperation Rate by Noise Level")
    print("-"*80)
    noise_summary = df.groupby('noise')['strategy'].apply(lambda x: (x == 'Cooperate').mean())
    for noise_level, coop_rate in noise_summary.items():
        print(f"ε = {noise_level:.0%}:  {coop_rate:.1%} cooperation")
    
    # Statistical test: Does noise affect cooperation?
    if len(df['noise'].unique()) > 1:
        groups = [df[df['noise'] == n]['strategy'].apply(lambda x: 1 if x == 'Cooperate' else 0) 
                 for n in sorted(df['noise'].unique())]
        
        if len(groups) >= 2:
            f_stat, p_value = stats.f_oneway(*groups)
            print(f"\nANOVA Test (Noise effect on cooperation):")
            print(f"  F-statistic: {f_stat:.3f}")
            print(f"  p-value: {p_value:.4f}")
            
            if p_value < 0.05:
                print(f"  Result: Statistically significant (p < 0.05)")
            else:
                print(f"  Result: Not significant (p >= 0.05)")
    
    # Table 4: Trembling Robustness Score
    print("\n### TABLE 4: Trembling Robustness Score")
    print("-"*80)
    
    noise_levels = []
    coop_rates = []
    for noise in sorted(df['noise'].unique()):
        noise_df = df[df['noise'] == noise]
        coop_rate = (noise_df['strategy'] == 'Cooperate').mean()
        noise_levels.append(noise)
        coop_rates.append(coop_rate)
    
    if len(noise_levels) >= 2:
        slope, intercept = np.polyfit(noise_levels, coop_rates, 1)
        print(f"Trembling Robustness Score (R): {slope:.3f}")
        print(f"Baseline Cooperation (ε=0 intercept): {intercept:.3f}")
        print(f"\nInterpretation:")
        if slope > -0.5:
            print("  - Highly ROBUST: Coalition survives noise well")
        elif slope > -2:
            print("  - MODERATE: Some degradation with noise")
        else:
            print("  - FRAGILE: Coalition collapses under noise")

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    # Part 1: Load data
    df, experiments = load_all_data()
    
    if len(df) == 0:
        print("\nNo data found! Check Output_Exp/ folder")
        return
    
    # Part 2: Behavioral dimensions
    behavior_df = calculate_behavioral_dimensions(df)
    
    # Part 3: Strategic patterns
    pattern_df = analyze_strategic_patterns(df)
    
    # Part 4: Reasoning analysis
    reasoning_data = analyze_reasoning_semantics(df)
    
    # Part 5: Meta-prompt validation
    meta_df = analyze_meta_prompts(df)
    
    # Part 6: Visualizations
    create_comprehensive_visualizations(df, behavior_df, reasoning_data)
    
    # Part 7: Statistical tables
    generate_statistical_summary(df, behavior_df)
    
    # Final summary
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE!")
    print("="*80)
    print("\nGenerated Outputs:")
    print("  - fig1_behavioral_dimensions.png")
    print("  - fig2_temporal_dynamics.png")
    print("  - fig3_behavioral_heatmap.png")
    print("  - fig4_reasoning_keywords.png")
    print("  - fig5_agent_comparison.png")
    print("\nAll files saved to Output_Exp/")
    print("\nReady for paper writing!")

if __name__ == "__main__":
    main()

