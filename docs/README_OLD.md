# Project Triad: Multi-Agent LLM Experiments

This project implements the experiments for "Project Triad", focusing on strategic robustness and fairness emergence in 3-player LLM games.

## Quick Start

### 1. Installation

```bash
pip install -r requirements.txt
```

### 2. Running Experiments

The main script `triad_experiment.py` supports running both Public Goods Game (PGG) and Triadic Prisoner's Dilemma (PD).

#### Public Goods Game (PGG) - 3 Players
Default mode. Runs the standard PGG.

```bash
python triad_experiment.py --game PGG --model MockModel --rounds 10
```

#### Triadic Prisoner's Dilemma (PD)
Runs the 3-player Prisoner's Dilemma as described in the research plan.

```bash
python triad_experiment.py --game PD --model MockModel --rounds 10
```

### Models Supported
- `MockModel`: Random behavior (no API key needed).
- `OpenAIGPT4o`: Requires `API_KEY_OPENAI` env variable.
- `Claude35Haiku`: Requires `API_KEY_ANTHROPIC` env variable.
- `MistralLarge`: Requires `API_KEY_MISTRAL` env variable.

## Structure

- `triad_experiment.py`: Standalone script containing the Game Engine (FairGame), Agents, and Experiment Logic.
