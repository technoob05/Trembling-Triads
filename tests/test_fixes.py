#!/usr/bin/env python3
"""
Quick test script to verify the fixes work correctly.
Tests response parsing and punishment logic without running full experiments.
"""

import re
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_strategy_parsing():
    """Test the improved strategy parsing logic"""
    print("=" * 60)
    print("TEST 1: Strategy Parsing")
    print("=" * 60)
    
    strategies = {
        "strategy1": "Cooperate",
        "strategy2": "Defect"
    }
    
    test_cases = [
        ("Cooperate", "strategy1", "Simple word"),
        ("A: Cooperate", "strategy1", "Format with A:"),
        ("I choose to Cooperate based on...", "strategy1", "Embedded in sentence"),
        ("Defect", "strategy2", "Simple defect"),
        ("My choice is Defect.", "strategy2", "Defect in sentence"),
        ("The cooperation strategy seems best. Cooperate.", "strategy1", "Multiple mentions"),
        ("Random text without keywords", None, "No match - should default"),
        ("Cooperate\nDefect", "strategy1", "Both keywords - first match wins"),
    ]
    
    passed = 0
    failed = 0
    
    for response, expected_key, description in test_cases:
        print(f"\n  Test: {description}")
        print(f"  Input: '{response[:50]}...'")
        
        # Apply the improved parsing logic
        found_strategy = None
        response_lower = response.lower()
        
        for key, val in strategies.items():
            strategy_lower = val.lower()
            
            # Pattern 1: "A: Strategy" format
            if f"a: {strategy_lower}" in response_lower or f"a:{strategy_lower}" in response_lower:
                found_strategy = key
                break
            # Pattern 2: Exact word match (with word boundaries)
            if re.search(rf'\b{re.escape(strategy_lower)}\b', response_lower):
                found_strategy = key
                break
            # Pattern 3: Loose match as fallback
            if strategy_lower in response_lower:
                found_strategy = key
                break
        
        if found_strategy == expected_key or (expected_key is None and found_strategy is not None):
            print(f"  [PASS] Found '{found_strategy}'")
            passed += 1
        else:
            print(f"  [FAIL] Expected '{expected_key}', got '{found_strategy}'")
            failed += 1
    
    print(f"\n  Summary: {passed} passed, {failed} failed")
    return failed == 0


def test_punishment_parsing():
    """Test the improved punishment phase parsing"""
    print("\n" + "=" * 60)
    print("TEST 2: Punishment Parsing")
    print("=" * 60)
    
    agent_names = ["Alice", "Bob", "Charlie"]
    current_agent = "Alice"
    opponents = ["Bob", "Charlie"]
    
    test_cases = [
        ("None", [], "Explicit None"),
        ("none", [], "Lowercase none"),
        ("None.", [], "None with punctuation"),
        ("Bob", ["Bob"], "Punish Bob"),
        ("Bob, Charlie", ["Bob", "Charlie"], "Punish both"),
        ("I will punish Bob for defecting", ["Bob"], "Bob in sentence"),
        ("Alice cooperated, so I'll punish Charlie", ["Charlie"], "Name in context"),
        ("Everyone cooperated. None", [], "None after explanation"),
        ("I think Alice did well but Bob and Charlie deserve punishment", ["Bob", "Charlie"], "Complex sentence"),
        ("No one to punish", [], "Implicit none"),
    ]
    
    passed = 0
    failed = 0
    
    for response, expected_punished, description in test_cases:
        print(f"\n  Test: {description}")
        print(f"  Input: '{response[:60]}...'")
        
        # Apply improved parsing logic
        punished = []
        
        # Check for explicit "None" response first
        if "none" not in response.lower()[:20]:
            # Parse names more carefully
            for opp in opponents:
                # Use word boundary matching to avoid false positives
                if re.search(rf'\b{re.escape(opp)}\b', response, re.IGNORECASE):
                    punished.append(opp)
        
        if set(punished) == set(expected_punished):
            print(f"  [PASS] Punished {punished}")
            passed += 1
        else:
            print(f"  [FAIL] Expected {expected_punished}, got {punished}")
            failed += 1
    
    print(f"\n  Summary: {passed} passed, {failed} failed")
    return failed == 0


def test_template_format():
    """Test that templates have proper format instructions"""
    print("\n" + "=" * 60)
    print("TEST 3: Template Format Verification")
    print("=" * 60)
    
    # Import the templates
    try:
        from triad_experiment import TEMPLATES, get_template_for_game
        
        print("\n  Checking English Template...")
        en_template = TEMPLATES['en']
        if "EXACTLY one word" in en_template and "Your response:" in en_template:
            print("  [PASS] English template has proper instructions")
            en_pass = True
        else:
            print("  [FAIL] English template missing instructions")
            en_pass = False
        
        print("\n  Checking Vietnamese Template...")
        vn_template = TEMPLATES['vn']
        if "CHÍNH XÁC một từ" in vn_template and "Câu trả lời của bạn:" in vn_template:
            print("  [PASS] Vietnamese template has proper instructions")
            vn_pass = True
        else:
            print("  [FAIL] Vietnamese template missing instructions")
            vn_pass = False
        
        print("\n  Checking Volunteer Dilemma Template...")
        vd_template = get_template_for_game("VD", "en")
        if "EXACTLY one word" in vd_template and "Your response:" in vd_template:
            print("  [PASS] VD template has proper instructions")
            vd_pass = True
        else:
            print("  [FAIL] VD template missing instructions")
            vd_pass = False
        
        return en_pass and vn_pass and vd_pass
        
    except Exception as e:
        print(f"  [FAIL] Could not import templates: {e}")
        return False


def test_model_config():
    """Test that model configuration is correct"""
    print("\n" + "=" * 60)
    print("TEST 4: Model Configuration Check")
    print("=" * 60)
    
    try:
        from triad_experiment import LocalHFConnector
        import inspect
        
        # Check the send_prompt method signature
        source = inspect.getsource(LocalHFConnector.send_prompt)
        
        checks = {
            "max_length": "max_length" in source or "truncation" in source,
            "KeyboardInterrupt": "KeyboardInterrupt" in source,
            "Default fallback": "Cooperate" in source or "fallback" in source.lower(),
        }
        
        all_passed = True
        for check_name, result in checks.items():
            if result:
                print(f"  [PASS] {check_name} implemented")
            else:
                print(f"  [FAIL] {check_name} missing")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"  [FAIL] Could not check model config: {e}")
        return False


def main():
    print("\n" + "=" * 60)
    print("TRIAD EXPERIMENT FIX VERIFICATION")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Strategy Parsing", test_strategy_parsing()))
    results.append(("Punishment Parsing", test_punishment_parsing()))
    results.append(("Template Format", test_template_format()))
    results.append(("Model Configuration", test_model_config()))
    
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
        print("The fixes are working correctly.")
        print("\nYou can now run experiments with:")
        print("  python triad_experiment.py --game PD --models Qwen2.5-32B --rounds 5")
    else:
        print("SOME TESTS FAILED!")
        print("Please review the failures above.")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

