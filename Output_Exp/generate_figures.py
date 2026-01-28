"""
COMPREHENSIVE VISUALIZATION SUITE FOR PROJECT TRIAD
===================================================
Generates publication-quality figures for all three pillars:
1. Robustness Test (IPD)
2. Welfare Test (PGG)
3. Safety Test (VD)

Author: Project Triad Research Team
Date: January 28, 2026
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from pathlib import Path
from collections import defaultdict
import pandas as pd

# Set publication-quality style
plt.style.use('seaborn-v0_8-paper')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

OUTPUT_DIR = Path("d:/MultiplayerGame_FairGame/Project_Triad/Output_Exp")
FIGURES_DIR = OUTPUT_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)


def load_experiment_data(game_type):
    """Load all experiments for a given game type."""
    files = list(OUTPUT_DIR.glob(f"experiment_results_{game_type}_*.json"))
    data = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            data.append(json.load(f))
    return data


def extract_cooperation_rate(data, game_type="PD"):
    """Extract cooperation rate by noise level and language."""
    results = defaultdict(lambda: defaultdict(list))
    
    for experiment in data:
        for exp_name, exp_data in experiment.items():
            # Parse experiment name: e.g., "PD_Qwen2.5-32B_en_Noise0.0"
            parts = exp_name.split('_')
            lang = parts[2]  # 'en' or 'vn'
            noise = float(parts[-1].replace('Noise', ''))
            
            history = exp_data.get('history', {})
            total_actions = 0
            coop_actions = 0
            
            for round_name, round_data in history.items():
                for agent_data in round_data:
                    total_actions += 1
                    if game_type == "PD":
                        if agent_data.get('strategy') == 'Cooperate':
                            coop_actions += 1
                    elif game_type == "PGG":
                        if agent_data.get('strategy') == 'Contribute':
                            coop_actions += 1
                    elif game_type == "VD":
                        if agent_data.get('strategy') == 'Volunteer':
                            coop_actions += 1
            
            coop_rate = (coop_actions / total_actions * 100) if total_actions > 0 else 0
            results[lang][noise].append(coop_rate)
    
    return results


def extract_agent_behavior(data):
    """Extract per-agent cooperation rates."""
    agent_stats = defaultdict(lambda: {'cooperate': 0, 'defect': 0})
    
    for experiment in data:
        for exp_name, exp_data in experiment.items():
            history = exp_data.get('history', {})
            
            for round_name, round_data in history.items():
                for agent_data in round_data:
                    agent = agent_data.get('agent', 'Unknown')
                    strategy = agent_data.get('strategy', 'Unknown')
                    
                    if strategy in ['Cooperate', 'Contribute', 'Volunteer']:
                        agent_stats[agent]['cooperate'] += 1
                    elif strategy in ['Defect', 'Keep', 'Ignore']:
                        agent_stats[agent]['defect'] += 1
    
    return agent_stats


def calculate_shapley_values(data, game_type="PD"):
    """Simplified Shapley value approximation based on average contribution."""
    agent_payoffs = defaultdict(list)
    
    for experiment in data:
        for exp_name, exp_data in experiment.items():
            history = exp_data.get('history', {})
            
            for round_name, round_data in history.items():
                for agent_data in round_data:
                    agent = agent_data.get('agent', 'Unknown')
                    score = agent_data.get('score', 0)
                    agent_payoffs[agent].append(score)
    
    # Calculate average payoff per agent
    shapley_approx = {}
    avg_payoff = np.mean([np.mean(scores) for scores in agent_payoffs.values()])
    
    for agent, scores in agent_payoffs.items():
        agent_avg = np.mean(scores)
        shapley_approx[agent] = agent_avg - avg_payoff  # Deviation from average
    
    return shapley_approx


def plot_figure1_cooperation_vs_noise():
    """Figure 1: Cooperation Rate vs. Noise Level (All Games)."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    game_types = [("PD", "Prisoner's Dilemma"), 
                  ("PGG", "Public Goods Game"), 
                  ("VD", "Volunteer's Dilemma")]
    
    for idx, (game_code, game_name) in enumerate(game_types):
        ax = axes[idx]
        data = load_experiment_data(game_code)
        results = extract_cooperation_rate(data, game_code)
        
        for lang, noise_data in results.items():
            noise_levels = sorted(noise_data.keys())
            coop_rates = [np.mean(noise_data[n]) for n in noise_levels]
            coop_std = [np.std(noise_data[n]) for n in noise_levels]
            
            ax.errorbar(noise_levels, coop_rates, yerr=coop_std, 
                       marker='o', linewidth=2, capsize=5, 
                       label=f'{lang.upper()}')
        
        ax.set_xlabel('Noise Level (ε)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Cooperation Rate (%)', fontsize=11, fontweight='bold')
        ax.set_title(game_name, fontsize=12, fontweight='bold')
        ax.legend(loc='best', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_ylim([0, 100])
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "Figure1_Cooperation_vs_Noise.png", 
                bbox_inches='tight', facecolor='white')
    plt.savefig(FIGURES_DIR / "Figure1_Cooperation_vs_Noise.pdf", 
                bbox_inches='tight')
    print(f"✅ Saved: Figure1_Cooperation_vs_Noise.png")


def plot_figure2_agent_behavior():
    """Figure 2: Per-Agent Cooperation Rates (Stacked Bar Chart)."""
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    game_types = [("PD", "IPD"), ("PGG", "PGG"), ("VD", "VD")]
    
    for idx, (game_code, game_name) in enumerate(game_types):
        ax = axes[idx]
        data = load_experiment_data(game_code)
        agent_stats = extract_agent_behavior(data)
        
        agents = sorted(agent_stats.keys())
        coop_pcts = []
        defect_pcts = []
        
        for agent in agents:
            total = agent_stats[agent]['cooperate'] + agent_stats[agent]['defect']
            coop_pct = (agent_stats[agent]['cooperate'] / total * 100) if total > 0 else 0
            defect_pct = (agent_stats[agent]['defect'] / total * 100) if total > 0 else 0
            coop_pcts.append(coop_pct)
            defect_pcts.append(defect_pct)
        
        x = np.arange(len(agents))
        width = 0.6
        
        ax.bar(x, coop_pcts, width, label='Cooperate', color='#2ecc71', alpha=0.8)
        ax.bar(x, defect_pcts, width, bottom=coop_pcts, 
               label='Defect', color='#e74c3c', alpha=0.8)
        
        ax.set_xlabel('Agent', fontsize=11, fontweight='bold')
        ax.set_ylabel('Percentage (%)', fontsize=11, fontweight='bold')
        ax.set_title(f'{game_name} - Agent Behavior', fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(agents)
        ax.legend(loc='upper right', frameon=True, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        ax.set_ylim([0, 105])
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "Figure2_Agent_Behavior.png", 
                bbox_inches='tight', facecolor='white')
    plt.savefig(FIGURES_DIR / "Figure2_Agent_Behavior.pdf", 
                bbox_inches='tight')
    print(f"✅ Saved: Figure2_Agent_Behavior.png")


def plot_figure3_shapley_heatmap():
    """Figure 3: Shapley Value Heatmap (Alignment Gap)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    game_types = ["PD", "PGG", "VD"]
    shapley_matrix = []
    agents_list = []
    
    for game_code in game_types:
        data = load_experiment_data(game_code)
        shapley = calculate_shapley_values(data, game_code)
        
        if not agents_list:
            agents_list = sorted(shapley.keys())
        
        shapley_matrix.append([shapley.get(agent, 0) for agent in agents_list])
    
    shapley_df = pd.DataFrame(shapley_matrix, 
                              columns=agents_list, 
                              index=[f"{g} (Deviation)" for g in game_types])
    
    sns.heatmap(shapley_df, annot=True, fmt='.2f', cmap='RdYlGn', 
                center=0, linewidths=1, linecolor='black',
                cbar_kws={'label': 'Alignment Gap\n(Positive = Altruistic, Negative = Exploiter)'},
                ax=ax)
    
    ax.set_title('Shapley Value Analysis: Value Creation vs. Capture', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Agent', fontsize=12, fontweight='bold')
    ax.set_ylabel('Game Type', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "Figure3_Shapley_Heatmap.png", 
                bbox_inches='tight', facecolor='white')
    plt.savefig(FIGURES_DIR / "Figure3_Shapley_Heatmap.pdf", 
                bbox_inches='tight')
    print(f"✅ Saved: Figure3_Shapley_Heatmap.png")


def plot_figure4_language_comparison():
    """Figure 4: Language-Strategy Coupling (English vs. Vietnamese)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    game_types = ["PD", "PGG", "VD"]
    languages = ['en', 'vn']
    
    lang_results = {lang: [] for lang in languages}
    
    for game_code in game_types:
        data = load_experiment_data(game_code)
        results = extract_cooperation_rate(data, game_code)
        
        for lang in languages:
            if lang in results:
                # Average across all noise levels
                all_rates = []
                for noise_level, rates in results[lang].items():
                    all_rates.extend(rates)
                avg_rate = np.mean(all_rates) if all_rates else 0
                lang_results[lang].append(avg_rate)
            else:
                lang_results[lang].append(0)
    
    x = np.arange(len(game_types))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, lang_results['en'], width, 
                   label='English', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + width/2, lang_results['vn'], width, 
                   label='Vietnamese', color='#e67e22', alpha=0.8)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax.set_xlabel('Game Type', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Cooperation Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Language-Strategy Coupling Effect', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(["Prisoner's Dilemma", 'Public Goods', "Volunteer's Dilemma"])
    ax.legend(loc='upper right', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax.set_ylim([0, max(max(lang_results['en']), max(lang_results['vn'])) * 1.2])
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "Figure4_Language_Comparison.png", 
                bbox_inches='tight', facecolor='white')
    plt.savefig(FIGURES_DIR / "Figure4_Language_Comparison.pdf", 
                bbox_inches='tight')
    print(f"✅ Saved: Figure4_Language_Comparison.png")


def plot_figure5_trembling_robustness():
    """Figure 5: Trembling Robustness Score (TRS) Calculation."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    data = load_experiment_data("PD")
    results = extract_cooperation_rate(data, "PD")
    
    # Focus on English data for TRS calculation
    if 'en' in results:
        noise_levels = sorted(results['en'].keys())
        coop_rates = [np.mean(results['en'][n]) for n in noise_levels]
        
        # Linear regression to calculate TRS
        coefficients = np.polyfit(noise_levels, coop_rates, 1)
        trs = coefficients[0]  # Slope
        poly = np.poly1d(coefficients)
        
        # Plot data points
        ax.scatter(noise_levels, coop_rates, s=100, color='#e74c3c', 
                  zorder=3, label='Observed Data')
        
        # Plot trend line
        x_trend = np.linspace(min(noise_levels), max(noise_levels), 100)
        y_trend = poly(x_trend)
        ax.plot(x_trend, y_trend, '--', color='#2c3e50', linewidth=2, 
               label=f'Linear Fit (TRS = {trs:.3f})')
        
        # Annotate TRS
        mid_x = (min(noise_levels) + max(noise_levels)) / 2
        mid_y = poly(mid_x)
        ax.annotate(f'Trembling Robustness Score\\nTRS = {trs:.3f}\\n(Positive = Noise Helps)', 
                   xy=(mid_x, mid_y), xytext=(mid_x, mid_y + 5),
                   fontsize=11, fontweight='bold', color='#2c3e50',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3),
                   ha='center')
    
    ax.set_xlabel('Noise Level (ε)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cooperation Rate (%)', fontsize=12, fontweight='bold')
    ax.set_title('Trembling Robustness Score (TRS) Analysis', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='best', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "Figure5_Trembling_Robustness.png", 
                bbox_inches='tight', facecolor='white')
    plt.savefig(FIGURES_DIR / "Figure5_Trembling_Robustness.pdf", 
                bbox_inches='tight')
    print(f"✅ Saved: Figure5_Trembling_Robustness.png")


def generate_all_figures():
    """Generate all publication-quality figures."""
    print("\n" + "="*60)
    print("  GENERATING PUBLICATION-QUALITY FIGURES")
    print("="*60 + "\n")
    
    try:
        print("📊 Figure 1: Cooperation vs. Noise (All Games)...")
        plot_figure1_cooperation_vs_noise()
        
        print("📊 Figure 2: Agent Behavior Analysis...")
        plot_figure2_agent_behavior()
        
        print("📊 Figure 3: Shapley Value Heatmap...")
        plot_figure3_shapley_heatmap()
        
        print("📊 Figure 4: Language-Strategy Coupling...")
        plot_figure4_language_comparison()
        
        print("📊 Figure 5: Trembling Robustness Score...")
        plot_figure5_trembling_robustness()
        
        print("\n" + "="*60)
        print("  ✅ ALL FIGURES GENERATED SUCCESSFULLY")
        print(f"  📁 Location: {FIGURES_DIR}")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error generating figures: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    generate_all_figures()
