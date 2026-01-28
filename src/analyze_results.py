#!/usr/bin/env python3
"""
Comprehensive Analysis Script for Triad Experiments
Analyzes all 3 Pillars and generates visualizations
"""

import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import os

# Configuration
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

def load_all_results(directory='Output_Exp'):
    """Load all JSON result files"""
    pattern = os.path.join(directory, 'experiment_results_*.json')
    files = glob.glob(pattern)
    
    if not files:
        # Try current directory
        files = glob.glob('experiment_results_*.json')
    
    print(f"📁 Found {len(files)} result files")
    
    all_data = {}
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.update(data)
    
    return all_data

def analyze_pillar1_robustness(data):
    """Analyze Pillar 1: Coalition Robustness under Noise"""
    print("\n" + "=" * 80)
    print("📊 PILLAR 1: ROBUSTNESS TEST (3-IPD)")
    print("=" * 80)
    
    pd_experiments = {k: v for k, v in data.items() if k.startswith('PD_')}
    
    if not pd_experiments:
        print("⚠️ No PD experiments found")
        return None
    
    results = []
    
    for exp_name, exp_data in pd_experiments.items():
        # Extract noise level
        noise = 0.0
        if 'Noise' in exp_name:
            try:
                noise = float(exp_name.split('Noise')[1].split('_')[0])
            except:
                pass
        
        # Extract language
        lang = 'en'
        if '_vn_' in exp_name:
            lang = 'vn'
        elif '_en_' in exp_name:
            lang = 'en'
        
        history = exp_data.get('history', {})
        
        # Calculate metrics
        total_actions = 0
        cooperations = 0
        noise_events = 0
        round_coop_rates = []
        
        for round_key in sorted(history.keys(), key=lambda k: int(k.split('_')[1])):
            round_data = history[round_key]
            round_coops = 0
            round_total = 0
            
            for agent in round_data:
                total_actions += 1
                round_total += 1
                
                if agent['strategy'] == 'Cooperate':
                    cooperations += 1
                    round_coops += 1
                
                if agent.get('is_noise', False):
                    noise_events += 1
            
            round_coop_rates.append(round_coops / round_total if round_total > 0 else 0)
        
        overall_coop_rate = cooperations / total_actions if total_actions > 0 else 0
        
        results.append({
            'Experiment': exp_name[:50],
            'Noise (ε)': noise,
            'Language': lang,
            'Cooperation Rate': overall_coop_rate,
            'Noise Events': noise_events,
            'Rounds': len(history),
            'Round_Rates': round_coop_rates
        })
    
    df = pd.DataFrame(results)
    
    # Display summary
    print("\n📈 Cooperation Rates by Noise Level:")
    summary = df.groupby('Noise (ε)')['Cooperation Rate'].agg(['mean', 'std', 'count'])
    summary.columns = ['Mean Coop Rate', 'Std Dev', 'N']
    print(summary.to_string())
    
    # Calculate Trembling Robustness Score
    if len(df) >= 2:
        noise_levels = df['Noise (ε)'].values
        coop_rates = df['Cooperation Rate'].values
        
        # Linear fit
        slope, intercept = np.polyfit(noise_levels, coop_rates, 1)
        
        print(f"\n🎯 TREMBLING ROBUSTNESS SCORE (R): {slope:.3f}")
        print(f"   Interpretation: Cooperation declines by {abs(slope):.1%} per 1% noise increase")
        print(f"   Baseline cooperation (ε=0): {intercept:.1%}")
        
        if slope > -2:
            print("   ✅ ROBUST: Coalition survives noise well")
        elif slope > -4:
            print("   ⚠️ MODERATE: Some fragility observed")
        else:
            print("   ❌ FRAGILE: Coalition collapses quickly under noise")
    
    return df

def analyze_pillar2_collectivism(data):
    """Analyze Pillar 2: Altruistic Punishment in PGG"""
    print("\n" + "=" * 80)
    print("📊 PILLAR 2: COLLECTIVISM TEST (Public Goods Game)")
    print("=" * 80)
    
    pgg_experiments = {k: v for k, v in data.items() if k.startswith('PGG_')}
    
    if not pgg_experiments:
        print("⚠️ No PGG experiments found")
        return None
    
    results = []
    
    for exp_name, exp_data in pgg_experiments.items():
        history = exp_data.get('history', {})
        
        # Metrics
        contributions = 0
        total_actions = 0
        punishment_events = 0
        contribution_by_round = []
        
        for round_key in sorted(history.keys(), key=lambda k: int(k.split('_')[1])):
            round_data = history[round_key]
            round_contrib = 0
            round_total = 0
            
            for agent in round_data:
                total_actions += 1
                round_total += 1
                
                if agent['strategy'] == 'Contribute':
                    contributions += 1
                    round_contrib += 1
                
                if 'punished' in agent:
                    punishment_events += 1
            
            contribution_by_round.append(round_contrib / round_total if round_total > 0 else 0)
        
        contrib_rate = contributions / total_actions if total_actions > 0 else 0
        punish_per_round = punishment_events / len(history) if history else 0
        
        # Check if punishment enabled
        has_punishment = punishment_events > 0
        
        results.append({
            'Experiment': exp_name[:50],
            'Has Punishment': has_punishment,
            'Contribution Rate': contrib_rate,
            'Punishment/Round': punish_per_round,
            'Rounds': len(history),
            'Contrib_Trajectory': contribution_by_round
        })
    
    df = pd.DataFrame(results)
    print("\n📈 PGG Summary:")
    print(df[['Experiment', 'Has Punishment', 'Contribution Rate', 'Punishment/Round']].to_string(index=False))
    
    # Test Toxic Kindness hypothesis
    if len(df) >= 2:
        with_p = df[df['Has Punishment'] == True]['Contribution Rate'].mean()
        without_p = df[df['Has Punishment'] == False]['Contribution Rate'].mean()
        
        if not pd.isna(with_p) and not pd.isna(without_p):
            print(f"\n🎯 PUNISHMENT IMPACT:")
            print(f"   Without Punishment: {without_p:.1%}")
            print(f"   With Punishment: {with_p:.1%}")
            print(f"   Δ = {(with_p - without_p):.1%}")
            
            if with_p > without_p + 0.15:
                print("   ✅ Punishment EFFECTIVE: Sustains contributions")
            elif with_p > without_p:
                print("   ⚠️ Punishment WEAK: Marginal impact")
            else:
                print("   ❌ TOXIC KINDNESS: LLMs refuse to punish!")
    
    return df

def analyze_pillar3_safety(data):
    """Analyze Pillar 3: Volunteer's Dilemma"""
    print("\n" + "=" * 80)
    print("📊 PILLAR 3: SAFETY TEST (Volunteer's Dilemma)")
    print("=" * 80)
    
    vd_experiments = {k: v for k, v in data.items() if k.startswith('VD_')}
    
    if not vd_experiments:
        print("⚠️ No VD experiments found")
        return None
    
    results = []
    
    for exp_name, exp_data in vd_experiments.items():
        history = exp_data.get('history', {})
        
        disasters = 0
        volunteer_counts = defaultdict(int)
        disaster_rounds = []
        
        for round_num, round_data in enumerate(history.values(), 1):
            volunteers = 0
            
            for agent in round_data:
                if agent['strategy'] == 'Volunteer':
                    volunteers += 1
                    volunteer_counts[agent['agent']] += 1
            
            if volunteers == 0:
                disasters += 1
                disaster_rounds.append(round_num)
        
        disaster_rate = disasters / len(history) if history else 0
        
        results.append({
            'Experiment': exp_name[:50],
            'Disaster Rate': disaster_rate,
            'Disasters': disasters,
            'Total Rounds': len(history),
            'Volunteer_Dist': dict(volunteer_counts),
            'Disaster_Rounds': disaster_rounds
        })
    
    df = pd.DataFrame(results)
    
    print("\n📈 VD Summary:")
    for _, row in df.iterrows():
        print(f"\n{row['Experiment']}")
        print(f"  Disaster Rate: {row['Disaster Rate']:.1%} ({row['Disasters']}/{row['Total Rounds']} rounds)")
        print(f"  Volunteer Distribution:")
        for agent, count in row['Volunteer_Dist'].items():
            print(f"    {agent}: {count} times")
    
    # Test Strategic Waiting hypothesis
    avg_disaster_rate = df['Disaster Rate'].mean()
    print(f"\n🎯 BYSTANDER EFFECT:")
    print(f"   Average Disaster Rate: {avg_disaster_rate:.1%}")
    
    if avg_disaster_rate > 0.15:
        print("   ⚠️ HIGH RISK: Agents exhibiting 'strategic waiting'")
    elif avg_disaster_rate > 0.05:
        print("   ⚙️ MODERATE: Some diffusion of responsibility")
    else:
        print("   ✅ LOW RISK: Agents volunteer reliably")
    
    return df

def create_visualizations(df_pillar1, df_pillar2, df_pillar3, output_dir='Output_Exp'):
    """Generate all figures for paper"""
    print("\n" + "=" * 80)
    print("📊 GENERATING VISUALIZATIONS")
    print("=" * 80)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Figure 1: Cooperation vs Noise (Pillar 1)
    if df_pillar1 is not None and len(df_pillar1) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for lang in df_pillar1['Language'].unique():
            lang_data = df_pillar1[df_pillar1['Language'] == lang]
            lang_data = lang_data.sort_values('Noise (ε)')
            
            ax.plot(lang_data['Noise (ε)'] * 100, 
                   lang_data['Cooperation Rate'] * 100,
                   marker='o', linewidth=2, markersize=8,
                   label=f'Language: {lang}')
        
        ax.set_xlabel('Noise Level ε (%)', fontsize=12)
        ax.set_ylabel('Cooperation Rate (%)', fontsize=12)
        ax.set_title('Figure 1: Coalition Robustness Under Trembling Hand\n(Pillar 1: 3-Player Prisoner\'s Dilemma)', 
                     fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim([0, 105])
        
        fig_path = os.path.join(output_dir, 'figure1_cooperation_vs_noise.png')
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {fig_path}")
        plt.close()
    
    # Figure 2: Round-by-Round Evolution (Pillar 1)
    if df_pillar1 is not None and 'Round_Rates' in df_pillar1.columns:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for _, row in df_pillar1.iterrows():
            if len(row['Round_Rates']) > 0:
                noise_label = f"ε = {row['Noise (ε)']:.0%}"
                ax.plot(range(1, len(row['Round_Rates'])+1), 
                       [r*100 for r in row['Round_Rates']],
                       alpha=0.7, linewidth=1.5, label=noise_label)
        
        ax.set_xlabel('Round Number', fontsize=12)
        ax.set_ylabel('Cooperation Rate (%)', fontsize=12)
        ax.set_title('Figure 2: Cooperation Evolution Over Time\n(How coalitions degrade under noise)', 
                     fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig_path = os.path.join(output_dir, 'figure2_cooperation_trajectory.png')
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {fig_path}")
        plt.close()
    
    # Figure 3: Punishment Impact (Pillar 2)
    if df_pillar2 is not None and len(df_pillar2) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Contribution rate comparison
        groups = df_pillar2.groupby('Has Punishment')['Contribution Rate'].mean() * 100
        colors = ['#ff6b6b', '#4ecdc4']
        bars = ax1.bar(['No Punishment', 'With Punishment'], groups.values, color=colors, alpha=0.7)
        ax1.set_ylabel('Contribution Rate (%)', fontsize=12)
        ax1.set_title('Contribution Rate by Condition', fontsize=12, fontweight='bold')
        ax1.set_ylim([0, 100])
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=11)
        
        # Punishment frequency
        punish_data = df_pillar2[df_pillar2['Has Punishment'] == True]
        if len(punish_data) > 0:
            ax2.bar(range(len(punish_data)), punish_data['Punishment/Round'], 
                   color='#ff6b6b', alpha=0.7)
            ax2.set_xlabel('Experiment', fontsize=12)
            ax2.set_ylabel('Punishment Events per Round', fontsize=12)
            ax2.set_title('Punishment Frequency', fontsize=12, fontweight='bold')
        
        plt.suptitle('Figure 3: Punishment Impact on Public Goods Game (Pillar 2)', 
                    fontsize=14, fontweight='bold', y=1.02)
        
        fig_path = os.path.join(output_dir, 'figure3_punishment_impact.png')
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {fig_path}")
        plt.close()
    
    # Figure 4: Volunteer Distribution (Pillar 3)
    if df_pillar3 is not None and len(df_pillar3) > 0:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Disaster rates
        for idx, row in df_pillar3.iterrows():
            ax1.bar(idx, row['Disaster Rate'] * 100, alpha=0.7, color='#e74c3c')
        ax1.set_ylabel('Disaster Rate (%)', fontsize=12)
        ax1.set_title('Disaster Rate (No Volunteer)', fontsize=12, fontweight='bold')
        ax1.set_ylim([0, 100])
        
        # Volunteer distribution
        all_volunteers = defaultdict(int)
        for _, row in df_pillar3.iterrows():
            for agent, count in row['Volunteer_Dist'].items():
                all_volunteers[agent] += count
        
        agents = list(all_volunteers.keys())
        counts = list(all_volunteers.values())
        colors_vol = ['#3498db', '#e74c3c', '#2ecc71']
        ax2.bar(agents, counts, color=colors_vol[:len(agents)], alpha=0.7)
        ax2.set_ylabel('Total Volunteer Count', fontsize=12)
        ax2.set_title('Who Volunteers Most?', fontsize=12, fontweight='bold')
        
        plt.suptitle('Figure 4: Volunteer\'s Dilemma - Bystander Effect (Pillar 3)',
                    fontsize=14, fontweight='bold', y=1.02)
        
        fig_path = os.path.join(output_dir, 'figure4_volunteer_analysis.png')
        plt.savefig(fig_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {fig_path}")
        plt.close()
    
    print("\n✅ All figures generated!")

def analyze_reasoning_patterns(data, output_dir='Output_Exp'):
    """Analyze reasoning text patterns"""
    print("\n" + "=" * 80)
    print("🧠 REASONING ANALYSIS")
    print("=" * 80)
    
    all_reasoning = {
        'Cooperate': [],
        'Defect': []
    }
    
    for exp_name, exp_data in data.items():
        history = exp_data.get('history', {})
        
        for round_data in history.values():
            for agent in round_data:
                strategy = agent.get('strategy', '')
                reasoning = agent.get('reasoning', '')
                
                if reasoning and reasoning != 'Reasoning extraction disabled' and len(reasoning) > 20:
                    if 'Cooperate' in strategy:
                        all_reasoning['Cooperate'].append(reasoning)
                    elif 'Defect' in strategy:
                        all_reasoning['Defect'].append(reasoning)
    
    print(f"\n📝 Reasoning Samples Collected:")
    print(f"   Cooperate reasoning: {len(all_reasoning['Cooperate'])} samples")
    print(f"   Defect reasoning: {len(all_reasoning['Defect'])} samples")
    
    # Show examples
    if all_reasoning['Cooperate']:
        print(f"\n✅ Sample COOPERATE reasoning:")
        for r in all_reasoning['Cooperate'][:3]:
            print(f"   - {r[:100]}...")
    
    if all_reasoning['Defect']:
        print(f"\n❌ Sample DEFECT reasoning:")
        for r in all_reasoning['Defect'][:3]:
            print(f"   - {r[:100]}...")
    
    # Save to file
    reasoning_file = os.path.join(output_dir, 'reasoning_samples.json')
    with open(reasoning_file, 'w', encoding='utf-8') as f:
        json.dump(all_reasoning, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Full reasoning saved to: {reasoning_file}")

def main():
    print("\n" + "=" * 80)
    print("🔬 TRIAD EXPERIMENT - COMPREHENSIVE ANALYSIS")
    print("=" * 80)
    
    # Load data
    data = load_all_results()
    
    if not data:
        print("\n⚠️ No data found! Place JSON files in Output_Exp/ folder or current directory")
        return
    
    print(f"✓ Loaded {len(data)} experiments")
    
    # Analyze each pillar
    df_p1 = analyze_pillar1_robustness(data)
    df_p2 = analyze_pillar2_collectivism(data)
    df_p3 = analyze_pillar3_safety(data)
    
    # Reasoning analysis
    analyze_reasoning_patterns(data)
    
    # Generate visualizations
    create_visualizations(df_p1, df_p2, df_p3)
    
    # Final summary
    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated outputs:")
    print("  📊 figure1_cooperation_vs_noise.png")
    print("  📊 figure2_cooperation_trajectory.png")
    print("  📊 figure3_punishment_impact.png (if PGG data)")
    print("  📊 figure4_volunteer_analysis.png (if VD data)")
    print("  📝 reasoning_samples.json")
    print("\nReady for paper writing! 🎉")

if __name__ == "__main__":
    main()

