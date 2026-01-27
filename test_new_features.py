#!/usr/bin/env python3
"""
Test script for new features: Reasoning Extraction & Meta-Prompting
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

def test_reasoning_extraction():
    """Test that reasoning field is present in output"""
    print("=" * 60)
    print("TEST 1: Reasoning Extraction")
    print("=" * 60)
    
    try:
        from triad_experiment import FairGameFactory, PGG_CONFIG, get_template_for_game
        
        # Configure with reasoning enabled
        config = PGG_CONFIG.copy()
        config['nRounds'] = 2
        config['llm'] = 'MockModel'
        config['languages'] = ['en']
        config['promptTemplate'] = {'en': get_template_for_game('PGG', 'en')}
        config['extract_reasoning'] = True  # Enable reasoning
        
        # Run game
        factory = FairGameFactory()
        print("\n  Running game with reasoning extraction...")
        results = factory.create_and_run_games(config)
        
        # Check results
        game_result = list(results.values())[0]
        history = game_result['history']
        
        has_reasoning = False
        for round_key, round_data in history.items():
            for agent_data in round_data:
                if 'reasoning' in agent_data:
                    has_reasoning = True
                    reasoning = agent_data['reasoning']
                    print(f"  [OK] Found reasoning for {agent_data['agent']}: {reasoning[:50]}...")
        
        if has_reasoning:
            print("\n  [PASS] Reasoning extraction works!")
            return True
        else:
            print("\n  [FAIL] No reasoning found in output")
            return False
            
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_meta_prompting():
    """Test that meta-prompting validation is present"""
    print("\n" + "=" * 60)
    print("TEST 2: Meta-Prompting")
    print("=" * 60)
    
    try:
        from triad_experiment import FairGameFactory, TRIADIC_PD_CONFIG, get_template_for_game
        
        # Configure with meta-prompting enabled
        config = TRIADIC_PD_CONFIG.copy()
        config['nRounds'] = 3
        config['llm'] = 'MockModel'
        config['languages'] = ['en']
        config['promptTemplate'] = {'en': get_template_for_game('PD', 'en')}
        config['meta_prompt_enabled'] = True
        config['meta_prompt_rounds'] = [1, 3]  # Test at round 1 and 3
        config['extract_reasoning'] = False  # Disable reasoning for this test
        
        # Run game
        factory = FairGameFactory()
        print("\n  Running game with meta-prompting...")
        results = factory.create_and_run_games(config)
        
        # Check results
        game_result = list(results.values())[0]
        history = game_result['history']
        
        has_meta_prompt = False
        for round_key in ['round_1', 'round_3']:
            if round_key in history:
                round_data = history[round_key]
                for agent_data in round_data:
                    if 'meta_prompt_validation' in agent_data:
                        has_meta_prompt = True
                        meta = agent_data['meta_prompt_validation']
                        print(f"\n  [OK] Found meta-prompt for {agent_data['agent']} in {round_key}:")
                        print(f"    - Payoff: {meta.get('payoff_understanding', 'N/A')[:40]}...")
                        print(f"    - History: {meta.get('history_recall', 'N/A')[:40]}...")
                        print(f"    - Strategy: {meta.get('strategy_understanding', 'N/A')[:40]}...")
        
        if has_meta_prompt:
            print("\n  [PASS] Meta-prompting works!")
            return True
        else:
            print("\n  [FAIL] No meta-prompt validation found")
            return False
            
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_combined_features():
    """Test reasoning + meta-prompting together"""
    print("\n" + "=" * 60)
    print("TEST 3: Combined Features (Reasoning + Meta-Prompting)")
    print("=" * 60)
    
    try:
        from triad_experiment import FairGameFactory, VD_CONFIG, get_template_for_game
        
        # Configure with both features
        config = VD_CONFIG.copy()
        config['nRounds'] = 2
        config['llm'] = 'MockModel'
        config['languages'] = ['en']
        config['promptTemplate'] = {'en': get_template_for_game('VD', 'en')}
        config['meta_prompt_enabled'] = True
        config['meta_prompt_rounds'] = [1]
        config['extract_reasoning'] = True
        
        # Run game
        factory = FairGameFactory()
        print("\n  Running game with both features...")
        results = factory.create_and_run_games(config)
        
        # Check results
        game_result = list(results.values())[0]
        history = game_result['history']
        
        has_both = False
        round_data = history.get('round_1', [])
        for agent_data in round_data:
            has_reasoning = 'reasoning' in agent_data
            has_meta = 'meta_prompt_validation' in agent_data
            
            if has_reasoning and has_meta:
                has_both = True
                print(f"\n  [OK] {agent_data['agent']} has both features:")
                print(f"    Reasoning: {agent_data['reasoning'][:50]}...")
                print(f"    Meta-prompt: {list(agent_data['meta_prompt_validation'].keys())}")
        
        if has_both:
            print("\n  [PASS] Combined features work!")
            return True
        else:
            print("\n  [FAIL] Missing one or both features")
            return False
            
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_output_format():
    """Test that JSON output has correct structure"""
    print("\n" + "=" * 60)
    print("TEST 4: JSON Output Format")
    print("=" * 60)
    
    # Sample expected structure
    expected_fields = ['agent', 'strategy', 'score', 'reasoning']
    optional_fields = ['meta_prompt_validation', 'message', 'intended_strategy', 'is_noise']
    
    try:
        from triad_experiment import GameHistory
        
        # Create mock history
        history = GameHistory()
        history.update_round(1, 'Alice', {
            'strategy': 'Cooperate',
            'score': 7,
            'intended_strategy': 'Cooperate',
            'is_noise': False,
            'reasoning': 'Test reasoning'
        })
        
        # Test describe method
        output = history.describe()
        
        if 'round_1' not in output:
            print("  [FAIL] Missing round_1 in output")
            return False
        
        agent_data = output['round_1'][0]
        
        # Check required fields
        all_present = True
        for field in expected_fields:
            if field in agent_data:
                print(f"  [OK] Field '{field}' present")
            else:
                print(f"  [X] Field '{field}' MISSING")
                all_present = False
        
        if all_present:
            print("\n  [PASS] Output format correct!")
            return True
        else:
            print("\n  [FAIL] Some fields missing")
            return False
            
    except Exception as e:
        print(f"\n  [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "=" * 60)
    print("NEW FEATURES TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    print("\n[INFO] Running tests with MockModel (no GPU needed)...\n")
    
    results.append(("Reasoning Extraction", test_reasoning_extraction()))
    results.append(("Meta-Prompting", test_meta_prompting()))
    results.append(("Combined Features", test_combined_features()))
    results.append(("Output Format", test_output_format()))
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("\nNew features are ready to use:")
        print("  python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 5 --reasoning")
        print("  python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 5 --meta-prompt")
    else:
        print("SOME TESTS FAILED!")
        print("Please review the failures above.")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

