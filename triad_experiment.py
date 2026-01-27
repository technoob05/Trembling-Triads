# --- KAGGLE SETUP BLOCK ---
# If you are pasting this into a Kaggle Notebook, you can run this block to ensure dependencies are installed.
# Or the script will attempt to install them automatically.
"""
!pip install -q -U openai anthropic mistralai pandas torch transformers accelerate bitsandbytes
"""

import sys
import os
import re
import json
import abc
import time
import random
import subprocess
import importlib.util
from typing import Dict, Any, List, Tuple

# Optimize CUDA Memory
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

# Attempt to patch Unsloth early
try:
    import unsloth
    print("[INFO] Unsloth found and patched early.")
except ImportError:
    pass

# --- 1. AUTO-SETUP & ENVIRONMENT ---

REQUIRED_PACKAGES = [
    "openai", "anthropic", "mistralai", "pandas", 
    "torch", "transformers", "accelerate", "bitsandbytes"
]

def check_and_install_dependencies():
    """Checks for required packages and installs them if missing (useful for Kaggle/Colab)."""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        if importlib.util.find_spec(pkg) is None:
            missing.append(pkg)
    
    if missing:
        print(f"Missing packages detected: {missing}. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-U"] + missing)
            print("Dependencies installed successfully.")
        except Exception as e:
            print(f"WARNING: Automatic installation failed: {e}. Please install manually via '!pip install ...'")

# Run setup
check_and_install_dependencies()

# --- 2. LLM CONNECTORS ---

class AbstractConnector(abc.ABC):
    @abc.abstractmethod
    def send_prompt(self, prompt: str, max_tokens: int = None) -> str:
        pass

class OpenAIConnector(AbstractConnector):
    def __init__(self, provider_model: str, temperature: float = 1.0):
        self.api_key = os.getenv("API_KEY_OPENAI")
        self.provider_model = provider_model
        self.temperature = temperature
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        except ImportError:
            self.client = None

    def send_prompt(self, prompt: str, max_tokens: int = None) -> str:
        if not self.client:
            return "[Error: OpenAI API Key missing or module not installed]"
        messages = [{"role": "user", "content": prompt}]
        kwargs = {
            "model": self.provider_model,
            "temperature": self.temperature,
            "messages": messages
        }
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        completion = self.client.chat.completions.create(**kwargs)
        return completion.choices[0].message.content

class AnthropicConnector(AbstractConnector):
    def __init__(self, provider_model: str, max_tokens: int = 1024):
        self.api_key = os.getenv("API_KEY_ANTHROPIC")
        self.provider_model = provider_model
        self.default_max_tokens = max_tokens
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key) if self.api_key else None
        except ImportError:
            self.client = None

    def send_prompt(self, prompt: str, max_tokens: int = None) -> str:
        if not self.client:
            return "[Error: Anthropic API Key missing or module not installed]"
        response = self.client.messages.create(
            max_tokens=max_tokens or self.default_max_tokens,
            messages=[{"role": "user", "content": prompt}],
            model=self.provider_model,
        )
        return response.content[0].text

class MistralConnector(AbstractConnector):
    def __init__(self, provider_model: str):
        self.api_key = os.getenv("API_KEY_MISTRAL")
        self.provider_model = provider_model
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=self.api_key) if self.api_key else None
        except ImportError:
            self.client = None

    def send_prompt(self, prompt: str) -> str:
        if not self.client:
            return "[Error: Mistral API Key missing or module not installed]"
        response = self.client.chat.complete(
            model=self.provider_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class LocalHFConnector(AbstractConnector):
    """
    Connector for running HuggingFace models locally (e.g., on Kaggle H100).
    Uses bitsandbytes 4-bit quantization for efficiency if available.
    """
    _pipeline = None
    _model_name = None

    def __init__(self, provider_model: str):
        self.provider_model = provider_model
        # Singleton-ish pattern to avoid reloading model for every agent if same model
        if LocalHFConnector._model_name != provider_model:
            self._load_model()
    
    
    def _load_model(self):
        print(f"Loading Local Model: {self.provider_model} onto GPU...")
        
        # Aggressive Memory Cleanup
        import gc
        import torch
        gc.collect()
        torch.cuda.empty_cache()

        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
            
            # Debugging Path
            if os.path.exists(self.provider_model):
                print(f"[DEBUG] Model path exists: {self.provider_model}")
                # print(f"[DEBUG] Directory contents: {os.listdir(self.provider_model)}")
            else:
                print(f"[WARNING] Model path NOT FOUND on disk: {self.provider_model}. Attempting to download from HF Hub...")

            # 1. Try Loading with Unsloth (Preferred for GPT-OSS / Llama / Qwen)
            try:
                # Must import unsloth BEFORE transformers (if not already handled globally)
                from unsloth import FastLanguageModel
                print(f"[INFO] Unsloth detected. Attempting to load {self.provider_model} via FastLanguageModel...")
                
                model, tokenizer = FastLanguageModel.from_pretrained(
                    model_name = self.provider_model,
                    max_seq_length = 2048, # Increased for history context (was 1024)
                    dtype = None, # Auto
                    load_in_4bit = True,
                    trust_remote_code = True,
                    device_map = "auto",
                )
                
                # Unsloth optimization for inference
                FastLanguageModel.for_inference(model)
                
                LocalHFConnector._pipeline = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=15,  # Default low (overridden per prompt type)
                    do_sample=False,     # Deterministic for game responses
                    temperature=0.1,     # Lower temperature for more focused responses
                    top_p=0.9
                    # max_length removed to avoid conflict warning
                )
                LocalHFConnector._model_name = self.provider_model
                print("Model loaded successfully via Unsloth.")
                return 

            except Exception as e:
                print(f"[INFO] Unsloth load failed or not installed ({e}). Falling back to Transformers...")
                # Cleanup again if Unsloth partially loaded stuff
                gc.collect()
                torch.cuda.empty_cache()

            # 2. Fallback: Standard Transformers Loading
            # Handle 4-bit loading
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

            try:
                print(f"[INFO] Attempting to load with BitsAndBytes (4-bit)...")
                tokenizer = AutoTokenizer.from_pretrained(self.provider_model, trust_remote_code=True)
                model = AutoModelForCausalLM.from_pretrained(
                    self.provider_model,
                    quantization_config=bnb_config,
                    device_map="auto",
                    trust_remote_code=True,
                    local_files_only=os.path.exists(self.provider_model) 
                )
            except Exception as e:
                 # ... existing fallback logic ...
                if "quantized" in str(e) or "Config" in str(e):
                    print(f"[INFO] Model appears already quantized ({e}). Retrying without manual quantization...")
                    if 'tokenizer' not in locals():
                         # Try to recover tokenizer if it failed earlier
                         tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-70B-Instruct", trust_remote_code=True) 

                    model = AutoModelForCausalLM.from_pretrained(
                        self.provider_model,
                        device_map="auto",
                        trust_remote_code=True,
                        local_files_only=os.path.exists(self.provider_model) 
                    )
                else:
                    raise e
            
            LocalHFConnector._pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=15,  # Default low (overridden per prompt type)
                do_sample=False,    # Deterministic for game responses
                temperature=0.1,    # Lower temperature for more focused responses
                top_p=0.9
            )
            LocalHFConnector._model_name = self.provider_model
            print("Model loaded successfully.")
            
        except Exception as e:
            print(f"CRITICAL ERROR LOADING MODEL: {e}")
            raise e

    def send_prompt(self, prompt: str, max_tokens: int = None) -> str:
        """
        Send prompt with optional max_tokens override.
        Use low max_tokens for strategy, higher for reasoning/meta-prompts.
        """
        if not LocalHFConnector._pipeline:
             self._load_model()
        
        # Determine appropriate max_new_tokens
        if max_tokens is None:
            # Auto-detect based on prompt content
            if any(keyword in prompt for keyword in ["Your choice:", "Your response:", ">", "ONE WORD"]):
                max_tokens = 8  # Strategy choice - VERY short (1-2 words max)
            else:
                max_tokens = 80  # Reasoning/meta-prompts - longer
        
        print(f"  [Generating...] Input len: {len(prompt)} chars (max_tokens={max_tokens})", end="\r")
        try:
            # MUST pass generation_kwargs to override pipeline defaults
            sequences = LocalHFConnector._pipeline(
                prompt,
                max_new_tokens=max_tokens,  # This DOES get overridden
                min_new_tokens=1,
                num_return_sequences=1,
                eos_token_id=LocalHFConnector._pipeline.tokenizer.eos_token_id,
                pad_token_id=LocalHFConnector._pipeline.tokenizer.eos_token_id,
                truncation=True,
                return_full_text=False  # CRITICAL: Don't return prompt in output
            )
            
            # Extract generated text only
            if isinstance(sequences, list) and len(sequences) > 0:
                if 'generated_text' in sequences[0]:
                    result = sequences[0]['generated_text']
                else:
                    result = str(sequences[0])
            else:
                result = str(sequences)
            
            # Clean up
            result = result.strip()
            # Remove prompt if still present
            if prompt in result:
                result = result.replace(prompt, "").strip()
            
            print(f"  [Generated] Output len: {len(result)} chars (max={max_tokens})    ")
            return result
        except KeyboardInterrupt:
            print("\n[INFO] Generation interrupted by user (Ctrl+C)")
            raise  # Re-raise to stop the experiment
        except Exception as e:
            print(f"\n[ERROR] Generation failed: {e}")
            return "Cooperate"  # Default fallback instead of "{}"


class MockConnector(AbstractConnector):
    """For testing without API keys"""
    def __init__(self, provider_model: str):
        self.provider_model = provider_model

    def send_prompt(self, prompt: str, max_tokens: int = None) -> str:
        # Randomly choose consistent strategies for testing
        return random.choice(["Contribute", "Keep"])


MODEL_PROVIDER_MAP = {
    # API Providers
    "Claude35Haiku": (AnthropicConnector, "claude-3-5-haiku-20241022"),
    "MistralLarge": (MistralConnector, "mistral-large-latest"),
    "OpenAIGPT4o": (OpenAIConnector, "gpt-4o"),
    "MockModel": (MockConnector, "mock"),
    
    # Local HuggingFace Models (Kaggle/Colab)
    "Llama3-8B": (LocalHFConnector, "meta-llama/Meta-Llama-3-8B-Instruct"),
    "Llama3-70B": (LocalHFConnector, "meta-llama/Meta-Llama-3-70B-Instruct"),
    "Mistral-7B": (LocalHFConnector, "mistralai/Mistral-7B-Instruct-v0.3"),
    "Qwen2.5-7B": (LocalHFConnector, "Qwen/Qwen2.5-7B-Instruct"),
    "Qwen2.5-14B": (LocalHFConnector, "Qwen/Qwen2.5-14B-Instruct"),
    "Qwen2.5-32B": (LocalHFConnector, "Qwen/Qwen2.5-32B-Instruct"),
    "Qwen2.5-72B": (LocalHFConnector, "Qwen/Qwen2.5-72B-Instruct"),
    "DeepSeek-R1-8B": (LocalHFConnector, "deepseek-ai/DeepSeek-R1-Distill-Llama-8B"),
    "DeepSeek-R1-70B": (LocalHFConnector, "deepseek-ai/DeepSeek-R1-Distill-Llama-70B"),
    "Gemma2-9B": (LocalHFConnector, "google/gemma-2-9b-it"),
    "Gemma2-27B": (LocalHFConnector, "google/gemma-2-27b-it"),
    "GPT-OSS-120B": (LocalHFConnector, "unsloth/gpt-oss-120b"),
}

class ChatModelFactory:
    @staticmethod
    @staticmethod
    def get_model(model_name: str):
        # 1. Check Pre-defined Models
        provider_info = MODEL_PROVIDER_MAP.get(model_name)
        if provider_info:
            model_class, provider_model = provider_info
            return model_class(provider_model)
        
        # 2. Check if it's a Local Path (e.g. /kaggle/input/...) or HuggingFace ID not in map
        # If it looks like a path or just a string, we assume it's a LocalHFConnector model
        # This allows users to pass "/kaggle/input/qwen2.5/transformers/72b-instruct" directly
        if "/" in model_name or os.path.exists(model_name):
            print(f"[Factory] Detected custom model path/ID: {model_name}. Using LocalHFConnector.")
            return LocalHFConnector(model_name)

        raise ValueError(f"Unsupported model specified: {model_name}. Available: {list(MODEL_PROVIDER_MAP.keys())} OR provide a valid path.")

def execute_prompt(model_name: str, prompt: str, max_tokens: int = None) -> str:
    chat_model = ChatModelFactory.get_model(model_name)
    # Simple retry logic
    for _ in range(3):
        try:
            # Pass max_tokens if connector supports it (LocalHFConnector does)
            if hasattr(chat_model, 'send_prompt') and 'max_tokens' in chat_model.send_prompt.__code__.co_varnames:
                return chat_model.send_prompt(prompt, max_tokens=max_tokens)
            else:
                return chat_model.send_prompt(prompt)
        except Exception as e:
            print(f"Error calling LLM: {e}. Retrying...")
            time.sleep(2)
    raise RuntimeError(f"Failed to execute prompt with {model_name}")

# --- 3. CORE LOGIC ---

class GameHistory:
    def __init__(self):
        self.rounds = {}

    def update_round(self, round_number, agent_name, data):
        round_key = f'round_{round_number}'
        if round_key not in self.rounds:
            self.rounds[round_key] = {}
        self.rounds[round_key].setdefault(agent_name, {}).update(data)

    def describe(self):
        summary = {}
        sorted_round_keys = sorted(self.rounds.keys(), key=lambda k: int(k.split('_')[1]))
        for round_key in sorted_round_keys:
            agents_data = self.rounds[round_key]
            round_list = []
            for agent_name, data in agents_data.items():
                entry = {
                    "agent": agent_name,
                    "message": data.get("message"),
                    "intended_strategy": data.get("intended_strategy"), # Log intention
                    "is_noise": data.get("is_noise", False),            # Log noise event
                    "strategy": data.get("strategy"),                   # Log actual result
                    "score": data.get("score"),
                    "reasoning": data.get("reasoning", "No reasoning provided")  # Log reasoning
                }
                # Add meta-prompt data if available
                if "meta_prompt" in data:
                    entry["meta_prompt_validation"] = data["meta_prompt"]
                
                round_list.append(entry)
            summary[round_key] = round_list
        return summary

class PayoffMatrix:
    def __init__(self, matrix_data, language):
        self.matrix_data = matrix_data
        self.language = language

    @property
    def strategies(self):
        return self.matrix_data['strategies'][self.language]
    
    @property
    def weights(self):
        return self.matrix_data['weights']
    
    @property
    def matrix(self):
        return self.matrix_data['matrix']

    def get_combination_key(self, round_strategies):
        for combo_key, strat_keys in self.matrix_data['combinations'].items():
            if strat_keys == round_strategies:
                return combo_key
        # Fallback for unordered matching if needed, but standard is ordered
        raise ValueError(f"Combination {round_strategies} not found in matrix.")

    def attribute_scores(self, agents, round_strategies):
        combo_key = self.get_combination_key(round_strategies)
        weight_keys = list(self.matrix[combo_key])
        for agent in agents:
            if not weight_keys:
                break
            agent_weight = weight_keys.pop(0)
            agent.add_score(self.weights[agent_weight])

class Agent:
    def __init__(self, name: str, llm_service: str, personality: str, opponent_personality_prob: int):
        self.name = name
        self.strategies = []
        self.scores = []
        self.llm_service = llm_service
        self.personality = personality
        self.opponent_personality_prob = opponent_personality_prob

    def execute_round(self, prompt: str, max_tokens: int = None) -> str:
        return execute_prompt(self.llm_service, prompt, max_tokens=max_tokens)

    def add_strategy(self, strategy: str):
        self.strategies.append(strategy)

    def last_strategy(self) -> str:
        return self.strategies[-1] if self.strategies else None

    def add_score(self, score: int):
        self.scores.append(score)

    def last_score(self) -> int:
        return self.scores[-1] if self.scores else 0

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "llm_service": self.llm_service,
            "personality": self.personality,
            "opponent_personality_probability": self.opponent_personality_prob
        }

class PromptCreator:
    def __init__(self, lang, prompt_template, n_rounds, n_rounds_known, payoff_matrix):
        self.language = lang
        self.prompt_template = prompt_template
        self.n_rounds = n_rounds
        self.n_rounds_known = n_rounds_known
        self.payoff_matrix = payoff_matrix

    def _find_part(self, field_name):
        pattern = rf"\{{{field_name}\}}:\s*\[(.*?)\]"
        return re.search(pattern, self.prompt_template, flags=re.DOTALL)
    
    def _replace_part(self, part, replacement=None):
        if part:
            content = replacement if replacement is not None else part.group(1)
            self.prompt_template = self.prompt_template.replace(part.group(0), content)

    def _remove_part(self, part):
        if part:
            self.prompt_template = self.prompt_template.replace(part.group(0), '')

    def map_placeholders(self, agent_name, opponents, current_round, history):
        strategies_keys = list(self.payoff_matrix.strategies.keys())
        weight_keys = list(self.payoff_matrix.weights.keys())
        
        # Format history as concise string instead of full dict
        history_str = self._format_history_concise(history, agent_name, [o.name for o in opponents])
        
        values = {
            'currentPlayerName': agent_name,
            'currentRound': current_round,
            'history': history_str,
        }
        for i, key in enumerate(strategies_keys):
            values[f"strategy{i+1}"] = self.payoff_matrix.strategies[key]
        for i, key in enumerate(weight_keys):
            values[f"weight{i+1}"] = self.payoff_matrix.weights[key]
        for i, opp in enumerate(opponents, start=1):
            values[f"opponent{i}"] = opp.name
        
        # Add basic nRounds if strictly needed by simple templates
        values['nRounds'] = self.n_rounds
        return values
    
    def _format_history_concise(self, history, agent_name, opponent_names):
        """Format history as concise string to save tokens"""
        if not history:
            return "None (first round)"
        
        lines = []
        sorted_rounds = sorted(history.keys(), key=lambda k: int(k.split('_')[1]))
        
        for round_key in sorted_rounds:
            round_num = round_key.split('_')[1]
            round_data = history[round_key]
            
            # Extract strategies for this round
            strategies = {}
            for name in [agent_name] + opponent_names:
                if name in round_data:
                    strategies[name] = round_data[name].get('strategy', '?')
            
            # Format: "R1: You=C, Alice=C, Bob=D"
            you_strat = strategies.get(agent_name, '?')[0]  # First char only
            opp_strats = ", ".join([f"{n}={strategies.get(n, '?')[0]}" for n in opponent_names])
            lines.append(f"R{round_num}: You={you_strat}, {opp_strats}")
        
        return "\n".join(lines)

    def process_optional_parts(self, agent, opponents, pv_dict):
        # Intro
        intro = self._find_part('intro')
        if intro:
            if agent.personality == 'None': self._remove_part(intro)
            else:
                self._replace_part(intro)
                pv_dict['personality'] = agent.personality
        
        # Opponent Intro
        op_intro = self._find_part('opponentIntro')
        if op_intro:
             valid = any((o.opponent_personality_prob != 0 and o.personality != 'None') for o in opponents)
             if not valid: self._remove_part(op_intro)
             else:
                 self._replace_part(op_intro)
                 for i, o in enumerate(opponents, start=1):
                     pv_dict[f"opponentPersonality{i}"] = o.personality
                     pv_dict[f"opponentPersonalityProbability{i}"] = o.opponent_personality_prob

        # Game Length
        gl = self._find_part('gameLength')
        if gl:
            if self.n_rounds_known:
                self._replace_part(gl)
                pv_dict['nRounds'] = self.n_rounds
            else:
                self._remove_part(gl)

    def fill_template(self, agent, opponents, current_round, history, phase):
        pv_dict = self.map_placeholders(agent.name, opponents, current_round, history)
        self.process_optional_parts(agent, opponents, pv_dict)
        
        comm_match = self._find_part('communicate')
        choose_match = self._find_part('choose')
        
        if phase == 'communicate':
            if comm_match: self._replace_part(comm_match)
            if choose_match: self._remove_part(choose_match)
        elif phase == 'choose':
            if choose_match: self._replace_part(choose_match)
            if comm_match: self._remove_part(comm_match)
            
        return self.prompt_template.format(**pv_dict)

class GameRound:
    def __init__(self, game):
        self.game = game
        self.round_number = game.current_round

    def run(self):
        # Meta-Prompting: Test comprehension at specific rounds (like "Nicer than Human" paper)
        if self.game.meta_prompt_enabled and self.round_number in self.game.meta_prompt_rounds:
            self._execute_meta_prompts()
        
        # Phase 1: Communication (Optional)
        if self.game.agents_communicate:
            self._execute_communication_phase()

        # Phase 2: Action / Contribution
        round_strategies = []
        for agent in self.game.agents.values():
            prompt = self.create_prompt(agent, phase='choose')
            strategy = self._execute_agent_strategy(agent, prompt)
            round_strategies.append(strategy)
        
        # Calculate Phase 1 Scores
        self.game.payoff_matrix.attribute_scores(list(self.game.agents.values()), round_strategies)
        
        # Phase 3: Punishment (Conditional for PGG)
        if self.game.punishment_enabled:
            self._execute_punishment_phase(round_strategies)

        return round_strategies

    def _execute_meta_prompts(self):
        """
        Meta-prompting technique from 'Nicer than Human' paper to validate
        that agents understand game rules and can parse history.
        """
        print(f"\n>>> META-PROMPT VALIDATION (Round {self.round_number}) <<<")
        
        for agent in self.game.agents.values():
            opponents = [a for a in self.game.agents.values() if a != agent]
            
            # Question 1: Payoff Understanding
            payoff_q = f"""You are playing a game with payoffs. Answer briefly:
If you Cooperate and your opponent Defects, what happens to your score compared to if you both Cooperate?
Answer in one short sentence."""
            
            # Question 2: History Recall
            if self.round_number > 1:
                history_q = f"""Based on the game history so far, which opponent has defected the most?
Answer with just the name or 'None'."""
            else:
                history_q = None
            
            # Question 3: Strategy Understanding
            strategy_q = f"""What is your main goal in this game? Answer in one short sentence."""
            
            # Execute validation prompts with higher max_tokens for full answers
            try:
                print(f"  [{agent.name}] Testing payoff understanding...")
                payoff_ans = agent.execute_round(payoff_q, max_tokens=60)[:100]
                
                if history_q:
                    print(f"  [{agent.name}] Testing history recall...")
                    history_ans = agent.execute_round(history_q, max_tokens=30)[:100]
                else:
                    history_ans = "N/A (Round 1)"
                
                print(f"  [{agent.name}] Testing strategy understanding...")
                strategy_ans = agent.execute_round(strategy_q, max_tokens=60)[:100]
                
                # Log meta-prompt results
                self.game.history.update_round(self.round_number, agent.name, {
                    'meta_prompt': {
                        'payoff_understanding': payoff_ans,
                        'history_recall': history_ans,
                        'strategy_understanding': strategy_ans
                    }
                })
                
                print(f"  [{agent.name}] Meta-prompts completed.")
                
            except Exception as e:
                print(f"  [{agent.name}] Meta-prompt failed: {e}")
    
    def _execute_communication_phase(self):
        for agent in self.game.agents.values():
            prompt = self.create_prompt(agent, phase='communicate')
            message = agent.execute_round(prompt)
            self.game.history.update_round(self.round_number, agent.name, {
                'message_prompt': prompt, 'message': message
            })

    def _execute_punishment_phase(self, round_strategies):
        # 1. Reveal who did what
        # In a real rigorous setting, we'd form a specific prompt. 
        # For this prototype, we'll append the result to the history string dynamically or just ask directly.
        
        agents_list = list(self.game.agents.values())
        
        # Punishment map: who punishes whom
        # punishment_cost = 1, punishment_fine = 3
        
        for agent in agents_list:
            # Simple prompt construction for punishment
            # We assume the agent knows what happened based on the "History" (which usually updates after the round).
            # But here we are IN the round. We need to tell them the immediate outcome.
            
            # Identify Free Riders (Strategy 2)
            # This logic is PGG specific
            opponents = [a for a in agents_list if a != agent]
            
            # Construct a mini-prompt
            # "The round results are: [A: Contribute, B: Keep, C: Keep]. You are A. Do you want to pay 1 point to deduct 3 points from any free-rider? Output the name of the agent to punish, or 'None'."
            
            current_outcome_str = ", ".join([f"{a.name}: {a.last_strategy()}" for a in agents_list])
            
            punish_prompt = f"""
The contribution phase for Round {self.round_number} is over.
Results: {current_outcome_str}.
You are {agent.name}.
You have the option to punish players who acted selfishly (Free-riders who chose 'Keep' or 'Defect').
Cost to you: 1 point. Fine to them: 3 points.
You can punish multiple people by listing names (e.g., 'Bob, Charlie') or respond 'None' to punish no one.
Output ONLY the names or 'None'. Do NOT explain your reasoning.

Your response:"""
            # Execute with low max_tokens (just need names or "None")
            response = agent.execute_round(punish_prompt, max_tokens=20).strip()
            
            # Clean and truncate for display
            display_response = response[:100] + "..." if len(response) > 100 else response
            print(f"[{agent.name} - PUNISH PHASE] Response: {display_response}")
            
            # IMPROVED PARSING: More strict name detection
            # Check for explicit "None" response first
            if "none" in response.lower()[:20]:  # Check only first 20 chars for "None"
                continue
                
            # Parse names more carefully - look for names as separate words
            for opp in opponents:
                # Use word boundary matching to avoid false positives
                if re.search(rf'\b{re.escape(opp.name)}\b', response, re.IGNORECASE):
                    # Apply Punishment
                    agent.add_score(-1) # Cost
                    opp.add_score(-3)   # Fine
                    print(f"!!! PUNISHMENT: {agent.name} punished {opp.name} !!!")
                    
                    # Log event
                    self.game.history.update_round(self.round_number, agent.name, {'punished': opp.name})
                    self.game.history.update_round(self.round_number, opp.name, {'was_punished_by': agent.name})


    def create_prompt(self, agent, phase):
        opponents = [a for a in self.game.agents.values() if a != agent]
        creator = PromptCreator(
            self.game.language, self.game.prompt_template,
            self.game.n_rounds, self.game.n_rounds_known,
            self.game.payoff_matrix
        )
        
        # LIMIT HISTORY CONTEXT to prevent token overflow
        # Only keep last N rounds (default 10) to stay within model's context window
        history_limit = 10
        all_rounds = sorted(self.game.history.rounds.keys(), key=lambda k: int(k.split('_')[1]))
        recent_rounds = all_rounds[-history_limit:] if len(all_rounds) > history_limit else all_rounds
        limited_history = {k: self.game.history.rounds[k] for k in recent_rounds}
        
        return creator.fill_template(agent, opponents, self.round_number, limited_history, phase)
    
    # ... (rest of class)

    def _ask_reasoning(self, agent, chosen_strategy):
        """
        Ask agent to explain their reasoning AFTER they've made their choice.
        This avoids interfering with the strategy parsing.
        """
        opponents = [a for a in self.game.agents.values() if a != agent]
        opp_names = ", ".join([o.name for o in opponents])
        
        reasoning_prompt = f"""You just chose to {chosen_strategy} in round {self.round_number} while playing with {opp_names}.
In 1-2 short sentences, explain WHY you made this choice. What factors influenced your decision?

Your reasoning:"""
        
        try:
            # Use higher max_tokens for reasoning (80 tokens = ~50-60 words = 1-2 sentences)
            reasoning_response = agent.execute_round(reasoning_prompt, max_tokens=80)
            return reasoning_response.strip()[:300]  # Limit to 300 chars
        except Exception as e:
            print(f"[{agent.name}] Failed to get reasoning: {e}")
            return "Failed to extract reasoning"
    
    def _execute_agent_strategy(self, agent, prompt):
        # We handle retry at the execute_prompt level somewhat
        # Use VERY LOW max_tokens for strategy choice (just need "Cooperate" or "Defect")
        response = agent.execute_round(prompt, max_tokens=8)
        
        # Clean and truncate response for display
        display_response = response[:100] + "..." if len(response) > 100 else response
        print(f"[{agent.name}] Response: {display_response}")
        
        # IMPROVED PARSING: Look for exact strategy words more carefully
        # Try to extract from common formats like "A: Cooperate" or just "Cooperate"
        found_strategy = None
        response_lower = response.lower()
        
        # Try different extraction patterns
        for key, val in self.game.payoff_matrix.strategies.items():
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
        
        # Determine intended strategy
        if found_strategy:
            intended_strategy_key = found_strategy
        else:
            print(f"[{agent.name}] No exact strategy match found in response. Defaulting to first strategy.")
            intended_strategy_key = list(self.game.payoff_matrix.strategies.keys())[0]

        # Apply Noise (Trembling Hand)
        final_strategy_key = intended_strategy_key
        is_noise = False
        if self.game.noise > 0:
            if random.random() < self.game.noise:
                # Flip strategy! (Assume 2 strategies for now)
                all_keys = list(self.game.payoff_matrix.strategies.keys())
                # Pick something different
                others = [k for k in all_keys if k != intended_strategy_key]
                if others:
                    final_strategy_key = random.choice(others)
                    is_noise = True
                    print(f"!!! TREMBLING HAND: {agent.name} intended {intended_strategy_key} but slipped to {final_strategy_key} !!!")

        # Get reasoning AFTER strategy is determined (if reasoning extraction enabled)
        if self.game.extract_reasoning:
            chosen_strategy_name = self.game.payoff_matrix.strategies[final_strategy_key]
            reasoning = self._ask_reasoning(agent, chosen_strategy_name)
        else:
            reasoning = "Reasoning extraction disabled"

        # Save transient state to agent for logging
        agent.last_intended_strategy = self.game.payoff_matrix.strategies[intended_strategy_key]
        agent.last_is_noise = is_noise
        agent.last_reasoning = reasoning
        
        agent.add_strategy(self.game.payoff_matrix.strategies[final_strategy_key])
        return final_strategy_key

    def _update_round_history(self):
        for agent in self.game.agents.values():
            self.game.history.update_round(self.round_number, agent.name, {
                'strategy': agent.last_strategy(),
                'score': agent.last_score(),
                'intended_strategy': getattr(agent, 'last_intended_strategy', None),
                'is_noise': getattr(agent, 'last_is_noise', False),
                'reasoning': getattr(agent, 'last_reasoning', 'No reasoning provided')
            })

class FairGame:
    def __init__(self, name, language, agents, n_rounds, n_rounds_known,
                 payoff_matrix_data, prompt_template, stop_conditions, agents_communicate, 
                 noise=0.0, punishment_enabled=False, meta_prompt_enabled=False, 
                 meta_prompt_rounds=None, extract_reasoning=False):
        self.name = name
        self.language = language
        self.agents = agents
        self.n_rounds = int(n_rounds)
        self.n_rounds_known = n_rounds_known
        self.prompt_template = prompt_template
        self.stop_conditions = stop_conditions
        self.agents_communicate = agents_communicate
        self.noise = noise  # Noise probability
        self.punishment_enabled = punishment_enabled # Phase 2 Punishment
        self.meta_prompt_enabled = meta_prompt_enabled  # Meta-prompting for validation
        self.meta_prompt_rounds = meta_prompt_rounds or [1, 3, 5]  # Default rounds for validation
        self.extract_reasoning = extract_reasoning  # Ask for reasoning separately
        self.current_round = 1
        self.history = GameHistory()
        self.choices_made = []
        self.payoff_matrix = PayoffMatrix(payoff_matrix_data, language)

    def run_round(self):
        runner = GameRound(self)
        round_strategies = runner.run()
        self.choices_made.append(round_strategies)
        # Scores are attributed inside runner.run now if punishment is on? 
        # Wait, typical flow is attribute -> update history.
        # But for Punishment, we need attribution FIRST (phase 1), then Punishment (phase 2 - modification), then History.
        # So in run(), we moved attribution logic.
        # Let's clean this up. runner.run() does it all.
        
        runner._update_round_history()

    def stop_condition_is_met(self):
        if self.choices_made:
            last = self.choices_made[-1]
            combo = next((k for k, v in self.payoff_matrix.matrix_data['combinations'].items() if v == last), None)
            if combo in self.stop_conditions:
                return True
        return False

    def run(self):
        while self.current_round <= self.n_rounds and not self.stop_condition_is_met():
            print(f"--- Round {self.current_round} ---")
            self.run_round()
            self.current_round += 1
        return self.history

class FairGameFactory:
    """Simplified Factory that takes Dict config instead of reading files."""
    
    def create_and_run_games(self, config: Dict[str, Any]):
        games = self.create_games(config)
        results = {}
        for i, game in enumerate(games):
            print(f"STARTING GAME {i+1}/{len(games)}")
            history = game.run()
            results[f"game_{i+1}"] = {
                "description": game.name,
                "history": history.describe()
            }
        return results

    def create_games(self, config):
        # Flatten basic config for single game or minimal permutations
        # For the standalone script, we will support exact 1 configuration execution mostly
        # but here we keep strict compatibility with the permutation logic
        
        # 1. Generate Config Dataframe
        rows = []
        lang = config['languages'][0] # Assume 1 language for simplicity
        
        # Create 1 row per permutation
        # We assume specific agents are defined
        agent_names = config['agents']['names']
        personalities = config['agents']['personalities'][lang]
        probs = config['agents']['opponentPersonalityProb']
        
        # Simple Logic: 1 Game, exactly as specified in lists
        row = {
            "Language": lang,
            "LLM": config['llm']
        }
        for i, name in enumerate(agent_names):
            row[f"Agent{i+1}"] = name
            row[f"Personality{i+1}"] = personalities[i] if i < len(personalities) else "None"
            row[f"OpponentPersonalityProb{i+1}"] = probs[i] if i < len(probs) else 0
            
        return [self._create_single_game(config, row)]

    def _create_single_game(self, config, row):
        # Create Agents
        agents = {}
        i = 1
        while f"Agent{i}" in row:
            agents[row[f"Agent{i}"]] = Agent(
                row[f"Agent{i}"], row['LLM'], row[f"Personality{i}"], row[f"OpponentPersonalityProb{i}"]
            )
            i += 1
            
        return FairGame(
            config['name'],
            row['Language'],
            agents,
            config['nRounds'],
            config['nRoundsIsKnown'],
            config['payoffMatrix'],
            config['promptTemplate'][row['Language']],
            config.get('stopGameWhen', []),
            config.get('agentsCommunicate', False),
            noise=config.get('noise', 0.0),
            punishment_enabled=config.get('punishment_enabled', False),
            meta_prompt_enabled=config.get('meta_prompt_enabled', False),
            meta_prompt_rounds=config.get('meta_prompt_rounds', [1, 3, 5]),
            extract_reasoning=config.get('extract_reasoning', False)
        )

# --- 4. EXPERIMENT SETUP (TEMPLATES & CONFIGS) ---

TEMPLATES = {
    "en": """
You are {currentPlayerName}. Playing with {opponent1} and {opponent2}.
{intro}: [Personality: {personality}]
Round {currentRound}/{nRounds}.

PAYOFFS:
All {strategy1} → {weight1} each
You {strategy2}, others {strategy1} → You: {weight2}, Them: {weight3}
All {strategy2} → {weight4} each

RECENT HISTORY:
{history}

Goal: Maximize your score.
{choose}: [Output EXACTLY one word: "{strategy1}" or "{strategy2}". No explanations.]

Your response:""",
    "vn": """
Bạn là {currentPlayerName}. Chơi với {opponent1} và {opponent2}.
{intro}: [Tính cách: {personality}]
Vòng {currentRound}/{nRounds}.

ĐIỂM SỐ:
Tất cả {strategy1} → {weight1} điểm mỗi người
Bạn {strategy2}, người khác {strategy1} → Bạn: {weight2}, Họ: {weight3}
Tất cả {strategy2} → {weight4} điểm mỗi người

LỊCH SỬ GẦN ĐÂY:
{history}

Mục tiêu: Tối đa hóa điểm.
{choose}: [CHỈ xuất CHÍNH XÁC một từ: "{strategy1}" hoặc "{strategy2}". Không giải thích.]

Câu trả lời của bạn:"""
}

def get_template_for_game(game_type, lang):
    """Selects the appropriate template based on game type and language."""
    if game_type == "VD":
        if lang == "vn":
            return """
Bạn là {currentPlayerName}. Đối thủ của bạn là {opponent1} và {opponent2}.
{intro}: [Bạn là người có tính cách: {personality}.]
{opponentIntro}: [{opponent1} có {opponentPersonalityProbability1}% khả năng là {opponentPersonality1}, {opponent2} có {opponentPersonalityProbability2}% khả năng là {opponentPersonality2}.]

Ba người các bạn đang trong tình thế nguy cấp. Nếu có ÍT NHẤT một người tình nguyện (Volunteer), cả nhóm sẽ an toàn—nhưng người tình nguyện phải trả một cái giá nhỏ. Nếu không ai tình nguyện, tất cả sẽ chịu phạt nặng. Các bạn không thể bàn bạc trước.

Mỗi vòng, các bạn chọn giữa '{strategy1}' (Tình nguyện) và '{strategy2}' (Làm ngơ).
{gameLength}: [Có {nRounds} vòng.]
Vòng hiện tại: {currentRound}.

Kết quả như sau:
– Nếu có ít nhất 1 người chọn {strategy1}: Những người chọn {strategy1} bị phạt {weight1} (-1), những người chọn {strategy2} không bị phạt (0).
– Nếu KHÔNG AI chọn {strategy1}: Tất cả bị phạt {weight2} (-5).

Mục tiêu: Tối đa hóa lợi ích cá nhân (giảm thiểu hình phạt).
Lịch sử: {history}.
{choose}: [CHỈ xuất ra CHÍNH XÁC một từ: '{strategy1}' hoặc '{strategy2}'. Không giải thích.]

Câu trả lời của bạn:"""
        else: # Default EN
            return """
You are {currentPlayerName}. Your opponents are {opponent1} and {opponent2}.
{intro}: [You are {personality}.]
{opponentIntro}: [{opponent1} has a probability of {opponentPersonalityProbability1}% of being {opponentPersonality1}.]

The three of you are in a critical situation. If at least one person volunteers, the group is safe—but the volunteer pays a cost. If no one volunteers, everyone suffers a much heavier penalty. You cannot coordinate your choices.

Each round, choose between '{strategy1}' (Volunteer) and '{strategy2}' (Ignore).
{gameLength}: [There are {nRounds} rounds.]
Current Round: {currentRound}.

Outcomes:
– If at least one person chooses {strategy1}: Volunteers get {weight1} (-1), Ignore gets 0.
– If NO ONE chooses {strategy1}: Everyone gets {weight2} (-5).

Goal: Maximize your personal outcome (minimize penalty).
History: {history}.
{choose}: [Output ONLY your choice - respond with EXACTLY one word: either '{strategy1}' or '{strategy2}'. No explanations.]

Your response:"""
    # Reuse generic templates for PGG/PD
    return TEMPLATES.get(lang, TEMPLATES['en'])


# 3-Player PGG Config
PGG3_PAYOFF = {
    "weights": {
        "GlobalWin": 10,   # All C
        "FreeRide": 12,    # D while others C
        "Sucker": 2,       # C while others D
        "PartialC": 6,     
        "PartialD": 8,
        "AllDefect": 4
    },
    "strategies": {
        "en": {"strategy1": "Contribute", "strategy2": "Keep"},
        "vn": {"strategy1": "Đóng góp", "strategy2": "Giữ lại"}
    },
    "combinations": {
        # Combinations for 3 players: [A1, A2, A3]
        "CCC": ["strategy1", "strategy1", "strategy1"],
        "CCD": ["strategy1", "strategy1", "strategy2"],
        "CDC": ["strategy1", "strategy2", "strategy1"],
        "DCC": ["strategy2", "strategy1", "strategy1"],
        "CDD": ["strategy1", "strategy2", "strategy2"],
        "DCD": ["strategy2", "strategy1", "strategy2"],
        "DDC": ["strategy2", "strategy2", "strategy1"],
        "DDD": ["strategy2", "strategy2", "strategy2"]
    },
    "matrix": {
        "CCC": ["GlobalWin", "GlobalWin", "GlobalWin"],
        "CCD": ["Sucker", "Sucker", "FreeRide"], 
        "CDC": ["Sucker", "FreeRide", "Sucker"],
        "DCC": ["FreeRide", "Sucker", "Sucker"],
        "CDD": ["Sucker", "FreeRide", "FreeRide"], 
        "DCD": ["FreeRide", "Sucker", "FreeRide"],
        "DDC": ["FreeRide", "FreeRide", "Sucker"],
        "DDD": ["AllDefect", "AllDefect", "AllDefect"]
    }
}

PGG_CONFIG = {
    "name": "Public Goods Game (3-Player)",
    "nRounds": 5, 
    "nRoundsIsKnown": True,
    "llm": "MockModel", 
    "languages": ["en"],
    "promptTemplate": None, # Will be set dynamically
    "agents": {
        "names": ["Alice", "Bob", "Charlie"],
        "personalities": {
            "en": ["Cooperative", "Selfish", "Tit-for-Tat"],
            "vn": ["Hợp tác", "Ích kỷ", "Ăn miếng trả miếng"]
        },
        "opponentPersonalityProb": [100, 100, 100]
    },
    "payoffMatrix": PGG3_PAYOFF,
    "punishment_enabled": True # Default to True for "PGG with Punishment"
}

# 3-Player Triadic PD Config (Updated per Research Proposal)
TRIADIC_PD_PAYOFF = {
    "weights": {
        "Reward": 7,       # CCC (All Cooperate)
        "Temptation": 9,   # D vs CC (Defector gets 9)
        "Sucker": 0,       # C vs DD (Lone Cooperator gets 0) - Matches Proposal "2 victims get 0"
        "Punishment": 1,   # DDD (All Defect)
        "LoneSucker": 0,   # C vs DD (Same as Sucker in this symmetric setup, usually)
        "Exploiter": 5     # D vs CD (Two Defectors get 5)
    },
    "strategies": {
        "en": {"strategy1": "Cooperate", "strategy2": "Defect"},
        "vn": {"strategy1": "Hợp tác", "strategy2": "Phản bội"}
    },
    "combinations": {
        "CCC": ["strategy1", "strategy1", "strategy1"],
        "CCD": ["strategy1", "strategy1", "strategy2"],
        "CDC": ["strategy1", "strategy2", "strategy1"],
        "DCC": ["strategy2", "strategy1", "strategy1"],
        "CDD": ["strategy1", "strategy2", "strategy2"],
        "DCD": ["strategy2", "strategy1", "strategy2"],
        "DDC": ["strategy2", "strategy2", "strategy1"],
        "DDD": ["strategy2", "strategy2", "strategy2"]
    },
    "matrix": {
        "CCC": ["Reward", "Reward", "Reward"],
        "CCD": ["Sucker", "Sucker", "Temptation"],
        "CDC": ["Sucker", "Temptation", "Sucker"],
        "DCC": ["Temptation", "Sucker", "Sucker"],
        "CDD": ["Sucker", "Exploiter", "Exploiter"], # C gets 0, D's get 5
        "DCD": ["Exploiter", "Sucker", "Exploiter"],
        "DDC": ["Exploiter", "Exploiter", "Sucker"],
        "DDD": ["Punishment", "Punishment", "Punishment"]
    }
}

TRIADIC_PD_CONFIG = PGG_CONFIG.copy()
TRIADIC_PD_CONFIG["name"] = "Triadic Prisoner's Dilemma"
TRIADIC_PD_CONFIG["payoffMatrix"] = TRIADIC_PD_PAYOFF
TRIADIC_PD_CONFIG["punishment_enabled"] = False  # PD has no punishment phase

# 3-Player Volunteer's Dilemma Config (Updated per Research Proposal)
VD_PAYOFF = {
    "weights": {
        "VolunteerNet": 80,   # 100 Benefit - 20 Cost
        "FreeRide": 100,      # 100 Benefit - 0 Cost
        "Disaster": -100      # Everyone dies
    },
    "strategies": {
        "en": {"strategy1": "Volunteer", "strategy2": "Ignore"},
        "vn": {"strategy1": "Tình nguyện", "strategy2": "Làm ngơ"}
    },
    "combinations": {
        "CCC": ["strategy1", "strategy1", "strategy1"],
        "CCD": ["strategy1", "strategy1", "strategy2"],
        "CDC": ["strategy1", "strategy2", "strategy1"],
        "DCC": ["strategy2", "strategy1", "strategy1"],
        "CDD": ["strategy1", "strategy2", "strategy2"],
        "DCD": ["strategy2", "strategy1", "strategy2"],
        "DDC": ["strategy2", "strategy2", "strategy1"],
        "DDD": ["strategy2", "strategy2", "strategy2"]
    },
    "matrix": {
        # Anyone who plays S1 (Volunteer) gets VolunteerNet
        # If no one plays S1, everyone gets Disaster
        # If someone volunteers, those who play S2 (Ignore) get FreeRide
        "CCC": ["VolunteerNet", "VolunteerNet", "VolunteerNet"], # All pay cost? Proposal says "All suffer cost", so 80.
        "CCD": ["VolunteerNet", "VolunteerNet", "FreeRide"],
        "CDC": ["VolunteerNet", "FreeRide", "VolunteerNet"],
        "DCC": ["FreeRide", "VolunteerNet", "VolunteerNet"],
        "CDD": ["VolunteerNet", "FreeRide", "FreeRide"],
        "DCD": ["FreeRide", "VolunteerNet", "FreeRide"],
        "DDC": ["FreeRide", "FreeRide", "VolunteerNet"],
        "DDD": ["Disaster", "Disaster", "Disaster"]
    }
}

VD_CONFIG = PGG_CONFIG.copy()
VD_CONFIG["name"] = "Volunteer's Dilemma (3-Player)"
VD_CONFIG["payoffMatrix"] = VD_PAYOFF
VD_CONFIG["punishment_enabled"] = False  # VD has no punishment phase


if __name__ == "__main__":
    import argparse
    import itertools
    import time # Added import for time
    import json # Added import for json


    parser = argparse.ArgumentParser(description="Run Triad Experiments")
    parser.add_argument("--game", type=str, default="PGG", choices=["PGG", "PD", "VD"], help="Game to play")
    parser.add_argument("--models", type=str, default="MockModel", help="Comma-separated model names")
    parser.add_argument("--rounds", type=int, default=5, help="Number of rounds")
    parser.add_argument("--languages", type=str, default="en", help="Comma-separated languages (en, vn)")
    parser.add_argument("--noise", type=float, default=0.0, help="Trembling Hand Noise Probability (0.0 to 1.0)")
    parser.add_argument("--punishment", action="store_true", help="Enable Punishment Phase (PGG only)")
    parser.add_argument("--no-punishment", dest="punishment", action="store_false", help="Disable Punishment Phase")
    parser.add_argument("--meta-prompt", action="store_true", help="Enable Meta-Prompting (comprehension validation)")
    parser.add_argument("--meta-rounds", type=str, default="1,3,5", help="Comma-separated rounds for meta-prompts (e.g., '1,3,5')")
    parser.add_argument("--reasoning", action="store_true", help="Extract reasoning from agents (separate prompt)")
    parser.set_defaults(punishment=True)

    args = parser.parse_args()

    # Select Base Config
    if args.game == "PGG":
        config = PGG_CONFIG
    elif args.game == "PD":
        config = TRIADIC_PD_CONFIG
    elif args.game == "VD":
        VD_PAYOFF_CONFIG = PGG_CONFIG.copy() # Quick hack to clone structure
        VD_PAYOFF_CONFIG["name"] = "Volunteer's Dilemma"
        VD_PAYOFF_CONFIG["payoffMatrix"] = VD_PAYOFF # Use the VD Payoff defined earlier
        VD_PAYOFF_CONFIG["punishment_enabled"] = False  # VD has no punishment
        config = VD_PAYOFF_CONFIG
    
    # Overrides
    config['nRounds'] = args.rounds
    config['noise'] = args.noise
    # Only override punishment for PGG (PD and VD don't have punishment)
    if args.game == "PGG":
        config['punishment_enabled'] = args.punishment
    config['meta_prompt_enabled'] = args.meta_prompt
    config['meta_prompt_rounds'] = [int(r.strip()) for r in args.meta_rounds.split(',')]
    config['extract_reasoning'] = args.reasoning
    
    # Multi-Model & Multi-Lang Loop
    models_list = args.models.split(',')
    languages_list = args.languages.split(',')
    
    factory = FairGameFactory()
    
    final_results = {}
    
    interrupted = False
    
    for model in models_list:
        if interrupted:
            break
            
        model = model.strip()
        config['llm'] = model
        
        for lang in languages_list:
            lang = lang.strip()
            
            # Temporary single-lang config for the factory
            run_config = config.copy()
            run_config['languages'] = [lang]
            run_config['promptTemplate'] = {lang: get_template_for_game(args.game, lang)} # Dynamic Template
            
            # Print actual punishment status from config, not args
            actual_punishment = run_config.get('punishment_enabled', False)
            print(f"\n>>> RUNNING EXPERIMENT: Game={args.game}, Model={model}, Lang={lang}, Noise={args.noise}, Punish={actual_punishment} <<<")
            
            # Adjust personalities map key to match single lang list
            # The factory expects config['agents']['personalities'][lang] to exist
            
            try:
                results = factory.create_and_run_games(run_config)
                
                # Tag results with metadata key
                for k, v in results.items():
                    key_name = f"{args.game}_{model}_{lang}_Noise{args.noise}"
                    final_results[key_name] = v
            except KeyboardInterrupt:
                print(f"\n\n!!! Experiment interrupted by user (Ctrl+C) !!!")
                print(f"Saving partial results before exit...")
                interrupted = True
                break  # Break inner loop
            except Exception as e:
                print(f"ERROR executing {model}/{lang}: {e}")
                import traceback
                traceback.print_exc()
                final_results[f"{args.game}_{model}_{lang}_ERROR"] = str(e)

    # Save Results
    timestamp = int(time.time())
    filename = f"experiment_results_{args.game}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nExperiment Complete. Results saved to {filename}")
