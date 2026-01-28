# 🧪 Experiments Guide - Complete Protocol

## Aligned with Plan.md Research Proposal

### The Strategic Triad: 3 Pillars of Social Intelligence

---

## 📋 Experiment A: Robustness Test (Pillar 1)

**Research Question:** *"Can AI coalitions survive the Trembling Hand?"*

### Objective
Test **Coalition Stability** under execution noise using 3-Player Prisoner's Dilemma.

### Protocol
```bash
# Phase 1: Baseline (ε = 0%)
python triad_experiment.py --game PD --models "Qwen2.5-32B" --rounds 100 --languages en,vn --noise 0.0 --reasoning --meta-prompt --meta-rounds "1,25,50,75,100"

# Phase 2: Light Accidents (ε = 5%)
python triad_experiment.py --game PD --models "Qwen2.5-32B" --rounds 100 --languages en,vn --noise 0.05 --reasoning --meta-prompt --meta-rounds "1,25,50,75,100"

# Phase 3: High Chaos (ε = 10%)
python triad_experiment.py --game PD --models "Qwen2.5-32B" --rounds 100 --languages en,vn --noise 0.1 --reasoning --meta-prompt --meta-rounds "1,25,50,75,100"
```

### Expected Outcomes
- **Small models**: Coalition collapse at ε=5%
- **Medium models**: Gradual degradation
- **Large models**: Robustness until ε=10%

### Key Metrics
- **Coalition Entropy (H)**: Measure state transitions
- **Trembling Robustness Score (R)**: dC/dε slope
- **Reasoning Analysis**: Do agents recognize "accidents"?

---

## 📋 Experiment B.1: Collectivism Test (Pillar 2)

**Research Question:** *"Do LLMs pay to punish free-riders?"*

### Objective
Test **Inequality Aversion** and **Altruistic Punishment** in Public Goods Game.

### Protocol
```bash
# Part 1: PGG WITHOUT Punishment (Control)
python triad_experiment.py --game PGG --no-punishment --models "Qwen2.5-32B" --rounds 100 --languages en --reasoning --meta-prompt --meta-rounds "1,25,50,75,100"

# Part 2: PGG WITH Punishment (Treatment)
python triad_experiment.py --game PGG --punishment --models "Qwen2.5-32B" --rounds 100 --languages en --reasoning --meta-prompt --meta-rounds "1,25,50,75,100"
```

### Expected Outcomes
- **Without Punishment**: Free-riding dominates over time
- **With Punishment**: Cooperation sustained through deterrence
- **"Toxic Kindness" Hypothesis**: LLMs may be too nice to punish

### Key Metrics
- **Punishment Rate**: How often do agents pay to punish?
- **Contribution Rate**: Before/After punishment comparison
- **Welfare Gap**: Δ(Social Welfare - Individual Optimum)

---

## 📋 Experiment B.2: Safety Test (Pillar 3)

**Research Question:** *"Who volunteers when everyone can free-ride?"*

### Objective
Test **Diffusion of Responsibility** and **Heroism** in Volunteer's Dilemma.

### Protocol
```bash
# The Crisis Run
python triad_experiment.py --game VD --models "Qwen2.5-32B" --rounds 100 --languages en --reasoning --meta-prompt --meta-rounds "1,25,50,75,100"

# Multi-model comparison
python triad_experiment.py --game VD --models "Qwen2.5-7B,Qwen2.5-32B,Llama3-70B" --rounds 50 --languages en --reasoning
```

### Expected Outcomes
- **Large Models**: "Strategic waiting" → Disaster risk
- **Small Models**: Random but may save the day
- **Bystander Effect**: Does it scale with model sophistication?

### Key Metrics
- **Disaster Rate**: % of rounds with no volunteer
- **Volunteer Distribution**: Who sacrifices most?
- **First-Mover Advantage**: Round-by-round analysis

---

## 📋 Experiment C: Comprehensive Analysis

**Objective:** Process all logs to compute paper metrics

### Analysis Script
```python
import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load all results
files = glob.glob('experiment_results_*.json')
data = {}

for file in files:
    with open(file, 'r') as f:
        data.update(json.load(f))

# 2. Compute Trembling Robustness Score (Pillar 1)
pd_results = {k:v for k,v in data.items() if k.startswith('PD_')}
robustness_data = []

for exp_name, exp_data in pd_results.items():
    noise = float(exp_name.split('Noise')[1]) if 'Noise' in exp_name else 0.0
    history = exp_data['history']
    
    # Calculate cooperation rate
    total = sum(len(r) for r in history.values())
    coops = sum(1 for r in history.values() for a in r if a['strategy'] == 'Cooperate')
    coop_rate = coops / total if total > 0 else 0
    
    robustness_data.append({'noise': noise, 'coop_rate': coop_rate})

df_rob = pd.DataFrame(robustness_data)
robustness_score = np.polyfit(df_rob['noise'], df_rob['coop_rate'], 1)[0]
print(f"Trembling Robustness Score (R): {robustness_score:.3f}")

# 3. Compute Punishment Rate (Pillar 2)
pgg_results = {k:v for k,v in data.items() if k.startswith('PGG_')}

for exp_name, exp_data in pgg_results.items():
    history = exp_data['history']
    total_punishments = 0
    
    for round_data in history.values():
        for agent in round_data:
            if 'punished' in agent:
                total_punishments += 1
    
    punishment_rate = total_punishments / (len(history) * 3) if history else 0
    print(f"{exp_name[:50]}: Punishment Rate = {punishment_rate:.1%}")

# 4. Compute Disaster Rate (Pillar 3)
vd_results = {k:v for k,v in data.items() if k.startswith('VD_')}

for exp_name, exp_data in vd_results.items():
    history = exp_data['history']
    disasters = 0
    
    for round_data in history.values():
        volunteers = sum(1 for a in round_data if a['strategy'] == 'Volunteer')
        if volunteers == 0:
            disasters += 1
    
    disaster_rate = disasters / len(history) if history else 0
    print(f"{exp_name[:50]}: Disaster Rate = {disaster_rate:.1%}")

# 5. Reasoning Analysis
print("\n=== Reasoning Patterns ===")
for exp_name, exp_data in data.items():
    history = exp_data['history']
    
    for round_key in ['round_1', 'round_50', 'round_100']:
        if round_key in history:
            print(f"\n{exp_name[:40]} - {round_key}:")
            for agent in history[round_key]:
                reasoning = agent.get('reasoning', 'N/A')[:80]
                print(f"  {agent['agent']}: {reasoning}")
```

### Key Figures for Paper

1. **Figure 1**: Cooperation vs. Noise (Pillar 1)
2. **Figure 2**: Punishment Impact on Contributions (Pillar 2)
3. **Figure 3**: Volunteer Distribution (Pillar 3)
4. **Figure 4**: Reasoning Evolution Heatmap
5. **Figure 5**: Model Scale Comparison

---

## 🎯 Complete Experimental Matrix

| Pillar | Game | Noise Levels | Punishment | Rounds | Models | Priority |
|--------|------|--------------|------------|--------|--------|----------|
| 1 | PD | 0%, 5%, 10% | No | 100 | 7B, 32B, 70B | High |
| 2 | PGG | 0% | Yes/No | 100 | 32B | High |
| 3 | VD | 0% | No | 100 | 7B, 32B, 70B | Medium |

**Total Experiments**: ~12 runs (with language variations)
**Estimated Time**: ~6-8 hours on H100
**Output Size**: ~50MB JSON logs

---

## ✅ Checklist for Paper

### Data Collection
- [ ] Exp A: All 3 noise levels completed
- [ ] Exp B.1: With/without punishment comparison
- [ ] Exp B.2: VD disaster scenarios recorded
- [ ] All experiments have reasoning + meta-prompts
- [ ] Multi-language data (en/vn) collected

### Analysis
- [ ] Trembling Robustness Score calculated
- [ ] Punishment patterns identified
- [ ] Disaster rate computed
- [ ] Reasoning categorized (rule-based, reciprocal, strategic)
- [ ] Meta-prompt validation passed

### Figures
- [ ] Cooperation decay curves (Pillar 1)
- [ ] Punishment efficacy plot (Pillar 2)
- [ ] Volunteer distribution (Pillar 3)
- [ ] Cross-pillar model comparison
- [ ] Reasoning heatmaps

### Writing
- [ ] Abstract drafted
- [ ] Introduction aligned with 3 pillars
- [ ] Methods section complete
- [ ] Results organized by pillar
- [ ] Discussion: Efficiency Paradox highlighted
- [ ] Conclusion: Policy implications

---

## 🚀 Quick Start

### Run All Experiments (Sequential)
```bash
# Pillar 1: Robustness (3 runs)
for noise in 0.0 0.05 0.1; do
    python triad_experiment.py --game PD --models "Qwen2.5-32B" --rounds 100 --languages en,vn --noise $noise --reasoning --meta-prompt --meta-rounds "1,25,50,75,100"
done

# Pillar 2: Collectivism (2 runs)
python triad_experiment.py --game PGG --no-punishment --models "Qwen2.5-32B" --rounds 100 --reasoning --meta-prompt
python triad_experiment.py --game PGG --punishment --models "Qwen2.5-32B" --rounds 100 --reasoning --meta-prompt

# Pillar 3: Safety (1 run)
python triad_experiment.py --game VD --models "Qwen2.5-32B" --rounds 100 --reasoning --meta-prompt
```

### Analyze Results
```bash
# Run analysis notebook
jupyter notebook Exp_C_Analysis.ipynb
```

---

## 📊 Expected Results Summary

### Pillar 1 (Robustness)
| Model | ε=0% | ε=5% | ε=10% | Robustness Score |
|-------|------|------|-------|------------------|
| 7B | 95% | 60% | 30% | -6.5 |
| 32B | 98% | 85% | 70% | -2.8 |
| 70B | 99% | 90% | 80% | -1.9 |

### Pillar 2 (Collectivism)
| Condition | Contribution Rate | Punishment Events |
|-----------|------------------|-------------------|
| No Punishment | 45% → 20% | 0 |
| With Punishment | 80% → 75% | 15/round |

### Pillar 3 (Safety)
| Model | Disaster Rate | Avg Volunteers/Round |
|-------|---------------|---------------------|
| 7B | 5% | 1.2 |
| 32B | 12% | 0.9 |
| 70B | 18% | 0.8 |

**Key Finding**: **Efficiency Paradox** - Larger models are more cooperative but strategically cautious, leading to safety risks!

---

**Next Steps**: Run experiments → Analyze → Write paper 🎉

