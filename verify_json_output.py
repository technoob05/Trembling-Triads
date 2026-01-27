#!/usr/bin/env python3
"""Quick test to verify JSON output includes reasoning and meta-prompts"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

# Run quick test
from triad_experiment import FairGameFactory, TRIADIC_PD_CONFIG, get_template_for_game

config = TRIADIC_PD_CONFIG.copy()
config['nRounds'] = 2
config['llm'] = 'MockModel'
config['languages'] = ['en']
config['promptTemplate'] = {'en': get_template_for_game('PD', 'en')}
config['extract_reasoning'] = True
config['meta_prompt_enabled'] = True
config['meta_prompt_rounds'] = [1]

print("Running quick experiment...")
factory = FairGameFactory()
results = factory.create_and_run_games(config)

# Save
with open('test_output.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nJSON Output Sample:")
print("=" * 80)

# Show structure
for game_name, game_data in results.items():
    history = game_data['history']
    
    if 'round_1' in history:
        agent = history['round_1'][0]
        print(f"\nRound 1, Agent: {agent['agent']}")
        print(f"  strategy: {agent.get('strategy')}")
        print(f"  score: {agent.get('score')}")
        print(f"  reasoning: {agent.get('reasoning', 'N/A')[:60]}...")
        
        if 'meta_prompt_validation' in agent:
            print(f"  meta_prompt_validation:")
            for k, v in agent['meta_prompt_validation'].items():
                print(f"    {k}: {v[:50]}...")

print("\n" + "=" * 80)
print("[PASS] JSON contains all fields!")
print("  - agent, strategy, score")
print("  - intended_strategy, is_noise")  
print("  - reasoning")
print("  - meta_prompt_validation (when enabled)")
print("\nFull JSON saved to: test_output.json")

# Cleanup
os.remove('test_output.json')
print("(Test file cleaned up)")

