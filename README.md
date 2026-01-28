# Triad Experiment - Multi-Agent Game Theory Research

Triadic game theory experiments with Large Language Models (Prisoner's Dilemma, Public Goods Game, Volunteer's Dilemma).

## 🚀 Quick Start

```bash
# Test với MockModel (không cần GPU)
python triad_experiment.py --game PD --models MockModel --rounds 5 --reasoning --meta-prompt

# Chạy với model thật (cần GPU)
python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 20 --reasoning --meta-prompt

# Test xem mọi thứ hoạt động chưa
python test_fixes.py
python test_new_features.py
```

---

## 📖 Documentation

**Tất cả tài liệu đã được tổ chức trong folder [`docs/`](docs/):**

### 🇻🇳 Tiếng Việt
- **[SUMMARY_VI.md](docs/SUMMARY_VI.md)** - Tổng quan toàn bộ features ⭐ **BẮT ĐẦU ĐÂY**
- **[TOM_TAT_SUA_LOI.md](docs/TOM_TAT_SUA_LOI.md)** - Chi tiết các bug fixes
- **[QUICK_START.md](docs/QUICK_START.md)** - Các lệnh thường dùng

### 🇬🇧 English
- **[NEW_FEATURES.md](docs/NEW_FEATURES.md)** - Reasoning Extraction & Meta-Prompting
- **[FIXES.md](docs/FIXES.md)** - Bug fixes and performance improvements

---

## 🎯 Features

### ✅ Core Functionality
- **3 Game Types**: Prisoner's Dilemma (PD), Public Goods Game (PGG), Volunteer's Dilemma (VD)
- **Multi-Model Support**: Llama, Qwen, Mistral, GPT, Claude, or any HuggingFace model
- **Multi-Language**: English, Vietnamese
- **Trembling Hand**: Noise injection for realistic behavior
- **Punishment Phase**: Optional punishment mechanism (PGG)

### 🆕 New Features (Inspired by "Nicer than Human" Paper)
- **Reasoning Extraction** - LLM explains WHY they chose each strategy
- **Meta-Prompting** - Validates that LLMs understand game rules
- **Comprehensive Logging** - JSON output with full game history

---

## 📊 Supported Models

### API-Based (Requires API Keys)
- `Claude35Haiku` - Anthropic
- `MistralLarge` - Mistral AI
- `OpenAIGPT4o` - OpenAI
- `MockModel` - Testing without API

### Local (HuggingFace - Requires GPU)
- `Qwen2.5-7B`, `Qwen2.5-14B`, `Qwen2.5-32B`, `Qwen2.5-72B`
- `Llama3-8B`, `Llama3-70B`
- `Mistral-7B`
- `DeepSeek-R1-8B`, `DeepSeek-R1-70B`
- `Gemma2-9B`, `Gemma2-27B`
- `GPT-OSS-120B`
- Any HuggingFace model path or ID

---

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

