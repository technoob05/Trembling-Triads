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
    def send_prompt(self, prompt: str) -> str:
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

    def send_prompt(self, prompt: str) -> str:
        if not self.client:
            return "[Error: OpenAI API Key missing or module not installed]"
        messages = [{"role": "user", "content": prompt}]
        completion = self.client.chat.completions.create(
            model=self.provider_model,
            temperature=self.temperature,
            messages=messages
        )
        return completion.choices[0].message.content

class AnthropicConnector(AbstractConnector):
    def __init__(self, provider_model: str, max_tokens: int = 1024):
        self.api_key = os.getenv("API_KEY_ANTHROPIC")
        self.provider_model = provider_model
        self.max_tokens = max_tokens
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key) if self.api_key else None
        except ImportError:
            self.client = None

    def send_prompt(self, prompt: str) -> str:
        if not self.client:
            return "[Error: Anthropic API Key missing or module not installed]"
        response = self.client.messages.create(
            max_tokens=self.max_tokens,
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
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, BitsAndBytesConfig
            
            # Quantization Config for H100/A100 optimization
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

            tokenizer = AutoTokenizer.from_pretrained(self.provider_model)
            model = AutoModelForCausalLM.from_pretrained(
                self.provider_model,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
            
            LocalHFConnector._pipeline = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=50, # Optimized for short strategy responses
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )
            LocalHFConnector._model_name = self.provider_model
            print("Model loaded successfully.")
            
        except Exception as e:
            print(f"CRITICAL ERROR LOADING MODEL: {e}")
            raise e

    def send_prompt(self, prompt: str) -> str:
        if not LocalHFConnector._pipeline:
            return "[Error: Model pipeline not initialized]"
        
        # Simple prompt formatting
        sequences = LocalHFConnector._pipeline(
            prompt,
            eos_token_id=LocalHFConnector._pipeline.tokenizer.eos_token_id,
            pad_token_id=LocalHFConnector._pipeline.tokenizer.eos_token_id
        )
        # Extract only the generated text (basic stripping)
        full_output = sequences[0]['generated_text']
        # Try to isolate the new part if possible, or just return the whole thing
        # Usually for chat models we need strict template application, but here we assume prompt is passed raw
        return full_output.replace(prompt, "").strip()


class MockConnector(AbstractConnector):
    """For testing without API keys"""
    def __init__(self, provider_model: str):
        self.provider_model = provider_model

    def send_prompt(self, prompt: str) -> str:
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
}

class ChatModelFactory:
    @staticmethod
    def get_model(model_name: str):
        provider_info = MODEL_PROVIDER_MAP.get(model_name)
        if not provider_info:
            raise ValueError(f"Unsupported model specified: {model_name}. Available: {list(MODEL_PROVIDER_MAP.keys())}")
        model_class, provider_model = provider_info
        return model_class(provider_model)

def execute_prompt(model_name: str, prompt: str) -> str:
    chat_model = ChatModelFactory.get_model(model_name)
    # Simple retry logic
    for _ in range(3):
        try:
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
                round_list.append({
                    "agent": agent_name,
                    "message": data.get("message"),
                    "intended_strategy": data.get("intended_strategy"), # Log intention
                    "is_noise": data.get("is_noise", False),            # Log noise event
                    "strategy": data.get("strategy"),                   # Log actual result
                    "score": data.get("score"),
                })
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

    def execute_round(self, prompt: str) -> str:
        return execute_prompt(self.llm_service, prompt)

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
        
        values = {
            'currentPlayerName': agent_name,
            'currentRound': current_round,
            'history': history,
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
You have the option to punish players who acted selfishly (Free-riders).
Cost to you: 1 point. Fine to them: 3 points.
You can punish multiple people (e.g., 'Bob, Charlie') or 'None'.
Output ONLY the names or 'None'.
"""
            # Execute
            response = agent.execute_round(punish_prompt)
            print(f"[{agent.name} - PUNISH PHASE] Response: {response}")
            
            # Parse names
            for opp in opponents:
                if opp.name in response:
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
        return creator.fill_template(agent, opponents, self.round_number, self.game.history.rounds, phase)
    
    # ... (rest of class)

    def _execute_agent_strategy(self, agent, prompt):
        # We handle retry at the execute_prompt level somewhat
        response = agent.execute_round(prompt)
        print(f"[{agent.name}] Response: {response}")
        found_strategy = next(
            (key for key, val in self.game.payoff_matrix.strategies.items()
             if val.lower() in response.lower()), None
        )
        
        # Determine intended strategy
        if found_strategy:
            intended_strategy_key = found_strategy
        else:
            print(f"[{agent.name}] No exact strategy match found. Defaulting to first strategy.")
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

        # Save transient state to agent for logging
        agent.last_intended_strategy = self.game.payoff_matrix.strategies[intended_strategy_key]
        agent.last_is_noise = is_noise
        
        agent.add_strategy(self.game.payoff_matrix.strategies[final_strategy_key])
        return final_strategy_key

    def _update_round_history(self):
        for agent in self.game.agents.values():
            self.game.history.update_round(self.round_number, agent.name, {
                'strategy': agent.last_strategy(),
                'score': agent.last_score(),
                'intended_strategy': getattr(agent, 'last_intended_strategy', None),
                'is_noise': getattr(agent, 'last_is_noise', False)
            })

class FairGame:
    def __init__(self, name, language, agents, n_rounds, n_rounds_known,
                 payoff_matrix_data, prompt_template, stop_conditions, agents_communicate, noise=0.0, punishment_enabled=False):
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
            punishment_enabled=config.get('punishment_enabled', False)
        )

# --- 4. EXPERIMENT SETUP (TEMPLATES & CONFIGS) ---

TEMPLATES = {
    "en": """
You are {currentPlayerName}. You are a participant in a game with {opponent1} and {opponent2}.
{intro}: [Your personality is: {personality}.]
{opponentIntro}: [You know that {opponent1} has a {opponentPersonalityProbability1}% chance of being {opponentPersonality1}.]

The game proceeds in rounds. There are {nRounds} rounds in total.
Current Round: {currentRound}.

You must choose between two options:
- '{strategy1}' (Cooperate / Contribute)
- '{strategy2}' (Defect / Keep)

Payoff Rules:
- If everyone chooses '{strategy1}', everyone gets {weight1}.
- If you choose '{strategy2}' but others choose '{strategy1}', you get {weight2} (Free rider) and they get {weight3} (Sucker).
- If everyone chooses '{strategy2}', everyone gets {weight4}.

History of previous rounds: 
{history}

Your goal is to maximize your own score over the long run.
{choose}: [Output ONLY your choice: '{strategy1}' or '{strategy2}'.]
""",
    "vn": """
Bạn là {currentPlayerName}. Bạn đang tham gia một trò chơi cùng với {opponent1} và {opponent2}.
{intro}: [Tính cách của bạn là: {personality}.]
{opponentIntro}: [Bạn biết rằng {opponent1} có {opponentPersonalityProbability1}% khả năng là người {opponentPersonality1}.]

Trò chơi diễn ra theo nhiều vòng. Tổng cộng có {nRounds} vòng.
Vòng hiện tại: {currentRound}.

Bạn phải chọn giữa hai phương án:
- '{strategy1}' (Hợp tác / Đóng góp)
- '{strategy2}' (Phản bội / Giữ lại)

Quy tắc trả thưởng:
- Nếu tất cả cùng chọn '{strategy1}', mỗi người nhận được {weight1}.
- Nếu bạn chọn '{strategy2}' nhưng những người khác chọn '{strategy1}', bạn nhận {weight2} (Hưởng lợi miễn phí) và họ nhận {weight3} (Người chịu thiệt).
- Nếu tất cả cùng chọn '{strategy2}', mỗi người nhận được {weight4}.

Lịch sử các vòng trước:
{history}

Mục tiêu của bạn là tối đa hóa điểm số của mình trong dài hạn.
{choose}: [CHỈ xuất ra lựa chọn của bạn: '{strategy1}' hoặc '{strategy2}'.]
"""
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
{choose}: [Chọn giữa {strategy1} và {strategy2}. CHỈ ghi lựa chọn.]
"""
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
{choose}: [Choose between {strategy1} and {strategy2}. Output ONLY the choice.]
"""
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
        config = VD_PAYOFF_CONFIG
    
    # Overrides
    config['nRounds'] = args.rounds
    config['noise'] = args.noise
    config['punishment_enabled'] = args.punishment
    
    # Multi-Model & Multi-Lang Loop
    models_list = args.models.split(',')
    languages_list = args.languages.split(',')
    
    factory = FairGameFactory()
    
    final_results = {}
    
    for model in models_list:
        model = model.strip()
        config['llm'] = model
        
        for lang in languages_list:
            lang = lang.strip()
            print(f"\n>>> RUNNING EXPERIMENT: Game={args.game}, Model={model}, Lang={lang}, Noise={args.noise}, Punish={args.punishment} <<<")
            
            # Temporary single-lang config for the factory
            run_config = config.copy()
            run_config['languages'] = [lang]
            run_config['promptTemplate'] = {lang: get_template_for_game(args.game, lang)} # Dynamic Template
            
            # Adjust personalities map key to match single lang list
            # The factory expects config['agents']['personalities'][lang] to exist
            
            try:
                results = factory.create_and_run_games(run_config)
                
                # Tag results with metadata key
                for k, v in results.items():
                    key_name = f"{args.game}_{model}_{lang}_Noise{args.noise}"
                    final_results[key_name] = v
            except Exception as e:
                print(f"ERROR executing {model}/{lang}: {e}")
                final_results[f"{args.game}_{model}_{lang}_ERROR"] = str(e)

    # Save Results
    timestamp = int(time.time())
    filename = f"experiment_results_{args.game}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    print(f"\nExperiment Complete. Results saved to {filename}")
