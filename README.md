# PROJECT TRIAD: Trembling Hands and Reluctant Heroes
## A Unified Game-Theoretic Framework for Multi-Agent LLM Evaluation

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![NeurIPS 2026](https://img.shields.io/badge/NeurIPS-2026-red.svg)](https://neurips.cc/)

Multi-agent game-theoretic experiments with Large Language Models across three strategic scenarios: Prisoner's Dilemma, Public Goods Game, and Volunteer's Dilemma.

---

## 🎯 One-Command Reproduction

```bash
# Install dependencies
pip install -r requirements.txt

# Reproduce entire paper (experiments + analysis + figures)
python reproduce_paper.py --mode all

# Or run components separately:
python reproduce_paper.py --mode experiments  # Run experiments only
python reproduce_paper.py --mode analysis     # Run analysis only
python reproduce_paper.py --mode figures      # Generate figures only
```

**Expected Output:**
- 6 experiment result files (~1.8 MB)
- COMPREHENSIVE_ANALYSIS.md (20-page research paper)
- 5 publication-quality figures (PNG + PDF)

**Time:** ~2-4 hours depending on API rate limits

---

## 🚀 Quick Start (Individual Experiments)

```bash
# Prisoner's Dilemma with noise
python triad_experiment.py --game PD --noise 0.05 --lang en --rounds 100

# Public Goods Game
python triad_experiment.py --game PGG --noise 0.0 --lang en --rounds 100

# Volunteer's Dilemma
python triad_experiment.py --game VD --noise 0.0 --lang en --rounds 100
```

---

## � Key Research Findings

### Three Paradoxes Discovered

1. **Trembling Paradox** - Noise increases cooperation by 12% (TRS = +0.20)
2. **Welfare Paradox** - "Toxic Kindness" enables exploitation (3:1 inequality)
3. **Heroism Paradox** - Strategic waiting causes bystander cascades (4% failures)

### Novel Metrics Introduced

- **TRS** (Trembling Robustness Score): Cooperation change per 1% noise
- **Alignment Gap**: Value created vs. captured (Shapley-based)
- **Coalition Entropy**: Alliance stability measure
- **Toxic Kindness Index**: Free-riding tolerance duration

### Publication-Ready Analysis

See [`Output_Exp/COMPREHENSIVE_ANALYSIS.md`](Output_Exp/COMPREHENSIVE_ANALYSIS.md) for the complete 20-page research paper with:
- Detailed methodology
- Statistical analysis
- Publication-quality figures
- Theoretical contributions

---

## 📖 Documentation Structure

### For Quick Start
- **[reproduce_paper.py](reproduce_paper.py)** - One-command reproduction ⭐
- **[QUICK_START.md](docs/QUICK_START.md)** - Basic usage examples

### For Researchers
- **[COMPREHENSIVE_ANALYSIS.md](Output_Exp/COMPREHENSIVE_ANALYSIS.md)** - Full 20-page paper
- **[EXECUTIVE_SUMMARY.md](Output_Exp/EXECUTIVE_SUMMARY.md)** - 1-page overview
- **[EXPERIMENTS_GUIDE.md](EXPERIMENTS_GUIDE.md)** - Detailed experiment documentation

### For Developers
- **[INDEX.md](INDEX.md)** - Complete project navigation
- **[Output_Exp/README.md](Output_Exp/README.md)** - Data structure guide
- **[test_new_features.py](test_new_features.py)** - Unit tests

---

## 🎯 Features & Capabilities

### ✅ Core Functionality
- **3 Game Types**: Prisoner's Dilemma (IPD), Public Goods Game (PGG), Volunteer's Dilemma (VD)
- **Noise Injection**: Trembling Hand mechanism (0-10% error rate)
- **Multi-Language**: English, Vietnamese, with extensibility for more
- **Reasoning Extraction**: LLMs explain strategic decisions
- **Meta-Prompting**: Validates game comprehension

### 🔬 Research Features
- **Shapley Value Analysis**: Individual contribution to welfare
- **Coalition Entropy**: Alliance stability metrics
- **Language-Strategy Coupling**: Cross-lingual behavioral analysis
- **Comprehensive Logging**: Full game history in structured JSON

---

## 🧪 Experimental Setup

### Agent Personalities
- **Alice**: Cooperative (always tries to cooperate)
- **Bob**: Selfish (maximizes own utility)
- **Charlie**: Tit-for-Tat (mirrors others' behavior)

### Supported Models
- **API-based**: Claude, GPT-4, Mistral Large
- **Local (requires GPU)**: Qwen 2.5 (7B-72B), Llama 3, Mistral, DeepSeek
- **Mock**: Testing without API/GPU

### Game Parameters
- Rounds: 1-1000 (default: 100)
- Noise: 0-100% (default: 0%)
- Language: en, vn
- With reasoning and meta-prompt validation

---

## 📊 Output Structure

```
Output_Exp/
├── experiment_results_PD_*.json      # Raw experimental data
├── experiment_results_PGG_*.json
├── experiment_results_VD_*.json
├── COMPREHENSIVE_ANALYSIS.md         # 20-page research paper
├── EXECUTIVE_SUMMARY.md              # 1-page overview
├── README.md                         # Data guide
└── figures/                          # Publication figures
    ├── Figure1_Cooperation_vs_Noise.png
    ├── Figure2_Agent_Behavior.png
    ├── Figure3_Shapley_Heatmap.png
    ├── Figure4_Language_Comparison.png
    └── Figure5_Trembling_Robustness.png
```

---

## 🛠️ Installation

### Requirements
- Python 3.10+
- GPU with 8GB+ VRAM (for local models)
- API keys for Claude/GPT/Mistral (for API models)

### Setup

```bash
# Clone repository
git clone https://github.com/technoob05/Trembling-Triads.git
cd Trembling-Triads/Project_Triad

# Install dependencies
pip install -r requirements.txt

# Set API keys (optional, for API-based models)
export API_KEY_ANTHROPIC="your-key"
export API_KEY_OPENAI="your-key"
export API_KEY_MISTRAL="your-key"

# Test installation
python test_new_features.py
```

---

## 📈 Citation

If you use this code or findings, please cite:

```bibtex
@article{projecttriad2026,
  title={Trembling Hands and Reluctant Heroes: A Unified Game-Theoretic 
         Framework for Robustness, Welfare, and Alignment in Multi-Agent LLMs},
  author={Project Triad Research Team},
  journal={In preparation for NeurIPS 2026},
  year={2026},
  url={https://github.com/technoob05/Trembling-Triads}
}
```

---

## 📜 License

MIT License - see [LICENSE](../LICENSE) for details.

---

## 🤝 Contributing

See [EXPERIMENTS_GUIDE.md](EXPERIMENTS_GUIDE.md) for contribution guidelines.

---

## 📞 Contact

- GitHub: https://github.com/technoob05/Trembling-Triads
- Issues: https://github.com/technoob05/Trembling-Triads/issues

---

**Status:** ✅ Clean, documented, and ready for NeurIPS 2026 submission  
**Last Updated:** January 28, 2026

## 🎮 Usage Examples

### Basic Games
```bash
# Prisoner's Dilemma
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10

# Public Goods Game with Punishment
python triad_experiment.py --game PGG --models Qwen2.5-32B --rounds 10 --punishment

# Volunteer's Dilemma
python triad_experiment.py --game VD --models Qwen2.5-32B --rounds 5
```

### Advanced Features
```bash
# With Reasoning Extraction
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --reasoning

# With Meta-Prompting (Comprehension Validation)
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 10 --meta-prompt --meta-rounds "1,5,10"

# Full Package (Everything)
python triad_experiment.py \
  --game PD \
  --models Qwen2.5-32B \
  --rounds 20 \
  --reasoning \
  --meta-prompt \
  --noise 0.1
```

### Multi-Model & Multi-Language
```bash
# Compare multiple models
python triad_experiment.py --game PD --models "Qwen2.5-32B,Llama3-70B" --rounds 10

# Multiple languages
python triad_experiment.py --game PD --models Qwen2.5-32B --languages "en,vn" --rounds 10
```

---

## 📁 Project Structure

```
Project_Triad/
├── triad_experiment.py          # Main script
├── test_fixes.py                # Test bug fixes
├── test_new_features.py         # Test new features
├── requirements.txt             # Python dependencies
│
├── docs/                        # 📖 All Documentation
│   ├── SUMMARY_VI.md           # ⭐ Hướng dẫn chính (Vietnamese)
│   ├── NEW_FEATURES.md         # Reasoning & Meta-prompting details
│   ├── FIXES.md                # Bug fixes documentation
│   ├── QUICK_START.md          # Command reference
│   └── TOM_TAT_SUA_LOI.md      # Bug fixes (Vietnamese)
│
├── Exp_A_Scale_Noise.ipynb     # Analysis: Scale & Noise
├── Exp_B_Games_MultiLang.ipynb # Analysis: Games & Languages
└── Exp_C_Analysis.ipynb        # Analysis: Comprehensive
```

---

## ✅ Testing

```bash
# Test bug fixes (parsing, punishment, etc.)
python test_fixes.py

# Test new features (reasoning, meta-prompting)
python test_new_features.py
```

**Expected output:** `ALL TESTS PASSED!`

---

## 📊 Output Format

Results are saved as JSON: `experiment_results_[GAME]_[TIMESTAMP].json`

### Example Output (with Reasoning & Meta-Prompting)
```json
{
  "PD_Qwen2.5-32B_en_Noise0.0": {
    "description": "Triadic Prisoner's Dilemma",
    "history": {
      "round_1": [
        {
          "agent": "Alice",
          "strategy": "Cooperate",
          "intended_strategy": "Cooperate",
          "is_noise": false,
          "score": 7,
          "reasoning": "I cooperated because starting with cooperation builds trust.",
          "meta_prompt_validation": {
            "payoff_understanding": "If I cooperate and opponent defects, I get sucker's payoff.",
            "history_recall": "N/A (Round 1)",
            "strategy_understanding": "Maximize my total score across all rounds."
          }
        }
      ]
    }
  }
}
```

---

## 🔧 Command-Line Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--game` | Game type (PGG, PD, VD) | `PGG` | `--game PD` |
| `--models` | Model names (comma-separated) | `MockModel` | `--models "Qwen2.5-32B,Llama3-70B"` |
| `--rounds` | Number of rounds | `5` | `--rounds 20` |
| `--languages` | Languages (comma-separated) | `en` | `--languages "en,vn"` |
| `--noise` | Trembling hand probability (0.0-1.0) | `0.0` | `--noise 0.1` |
| `--punishment` / `--no-punishment` | Enable/disable punishment | `True` | `--no-punishment` |
| `--reasoning` | Extract reasoning from agents | `False` | `--reasoning` |
| `--meta-prompt` | Validate comprehension | `False` | `--meta-prompt` |
| `--meta-rounds` | Rounds for meta-prompting | `"1,3,5"` | `--meta-rounds "1,10,20"` |

---

## 📚 Research Background

This project implements triadic game theory experiments inspired by:

**"Nicer than Human: How Do Large Language Models Behave in the Prisoner's Dilemma?"**
- *Conference*: ICWSM 2025
- *Authors*: Nicolò Fontana, Francesco Pierri, Luca Maria Aiello

### Key Contributions
1. **Meta-Prompting Validation** - Tests LLM comprehension of game rules
2. **Reasoning Extraction** - Captures LLM decision-making process
3. **Extended Gameplay** - Supports 100+ round experiments
4. **Behavioral Analysis** - Logs intended vs. actual strategies (with noise)

---

## 🔬 Analysis Notebooks

- **`Exp_A_Scale_Noise.ipynb`** - Analyze impact of model scale and noise
- **`Exp_B_Games_MultiLang.ipynb`** - Compare games and languages
- **`Exp_C_Analysis.ipynb`** - Comprehensive analysis

---

## 🛠️ Installation

```bash
# Clone the repository
cd Project_Triad

# Install dependencies (auto-installs on first run)
pip install -q -U openai anthropic mistralai pandas torch transformers accelerate bitsandbytes

# Optional: Install Unsloth for faster inference
pip install unsloth
```

### API Keys (if using API models)
```bash
export API_KEY_OPENAI="sk-..."
export API_KEY_ANTHROPIC="sk-..."
export API_KEY_MISTRAL="..."
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| CUDA out of memory | Use smaller model (7B instead of 32B) |
| Model generates too much text | Already fixed! Max tokens reduced to 10 |
| Parsing errors | Already fixed! Improved regex matching |
| False punishment | Already fixed! Word boundary detection |

**See [docs/FIXES.md](docs/FIXES.md) for details on all bug fixes.**

---

## 📞 Support

- **Documentation**: Check [`docs/`](docs/) folder
- **Tests**: Run `python test_fixes.py` and `python test_new_features.py`
- **Logs**: Save with `python triad_experiment.py 2>&1 | tee experiment.log`

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎉 Quick Links

- **[⭐ Bắt Đầu (Vietnamese)](docs/SUMMARY_VI.md)** - Comprehensive guide in Vietnamese
- **[🚀 Quick Start Guide](docs/QUICK_START.md)** - Common commands
- **[🆕 New Features](docs/NEW_FEATURES.md)** - Reasoning & Meta-prompting
- **[🔧 Bug Fixes](docs/FIXES.md)** - Performance improvements

---

**Happy Experimenting! 🎯**

```bash
# Let's go!
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 20 --reasoning --meta-prompt
```

