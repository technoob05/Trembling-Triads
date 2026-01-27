import os
import re
import json
import abc
import time
import random
from typing import Dict, Any, List, Tuple
from enum import Enum
from dataclasses import dataclass

# --- 1. SETTINGS & CONSTANTS ---

# Default API setup (User should replace these or set ENV variables)
# os.environ["API_KEY_OPENAI"] = "sk-..."
# os.environ["API_KEY_ANTHROPIC"] = "sk-..."

# --- 2. LLM CONNECTORS ---

class AbstractConnector(abc.ABC):
    @abc.abstractmethod
    def send_prompt(self, prompt: str) -> str:
        pass

class OpenAIConnector(AbstractConnector):
    def __init__(self, provider_model: str, temperature: float = 1.0):
        self.api_key = os.getenv("API_KEY_OPENAI")
        if not self.api_key:
            print("WARNING: API_KEY_OPENAI not set. OpenAI calls will fail.")
        self.provider_model = provider_model
        self.temperature = temperature
        # Lazy import to avoid hard dependency if not used
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            self.client = None

    def send_prompt(self, prompt: str) -> str:
        if not self.client:
            raise ImportError("openai module not installed.")
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
        if not self.api_key:
            print("WARNING: API_KEY_ANTHROPIC not set. Anthropic calls will fail.")
        self.provider_model = provider_model
        self.max_tokens = max_tokens
        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            self.client = None

    def send_prompt(self, prompt: str) -> str:
        if not self.client:
            raise ImportError("anthropic module not installed.")
        response = self.client.messages.create(
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
            model=self.provider_model,
        )
        return response.content[0].text

class MistralConnector(AbstractConnector):
    def __init__(self, provider_model: str):
        self.api_key = os.getenv("API_KEY_MISTRAL")
        if not self.api_key:
            print("WARNING: API_KEY_MISTRAL not set.")
        self.provider_model = provider_model
        try:
            from mistralai import Mistral
            self.client = Mistral(api_key=self.api_key)
        except ImportError:
            self.client = None

    def send_prompt(self, prompt: str) -> str:
        if not self.client:
            raise ImportError("mistralai module not installed.")
        response = self.client.chat.complete(
            model=self.provider_model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

class MockConnector(AbstractConnector):
    """For testing without API keys"""
    def __init__(self, provider_model: str):
        self.provider_model = provider_model

    def send_prompt(self, prompt: str) -> str:
        # Randomly choose consistent strategies for testing
        return random.choice(["Contribute", "Keep"])

MODEL_PROVIDER_MAP = {
    "Claude35Haiku": (AnthropicConnector, "claude-3-5-haiku-20241022"),
    "MistralLarge": (MistralConnector, "mistral-large-latest"),
    "OpenAIGPT4o": (OpenAIConnector, "gpt-4o"),
    "MockModel": (MockConnector, "mock"),
}

class ChatModelFactory:
    @staticmethod
    def get_model(model_name: str):
        provider_info = MODEL_PROVIDER_MAP.get(model_name)
        if not provider_info:
            raise ValueError(f"Unsupported model specified: {model_name}")
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
                    "strategy": data.get("strategy"),
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
        if self.game.agents_communicate:
            self._execute_communication_phase()

        round_strategies = []
        for agent in self.game.agents.values():
            prompt = self.create_prompt(agent, phase='choose')
            strategy = self._execute_agent_strategy(agent, prompt)
            round_strategies.append(strategy)
        return round_strategies

    def _execute_communication_phase(self):
        for agent in self.game.agents.values():
            prompt = self.create_prompt(agent, phase='communicate')
            message = agent.execute_round(prompt)
            self.game.history.update_round(self.round_number, agent.name, {
                'message_prompt': prompt, 'message': message
            })

    def create_prompt(self, agent, phase):
        opponents = [a for a in self.game.agents.values() if a != agent]
        creator = PromptCreator(
            self.game.language, self.game.prompt_template,
            self.game.n_rounds, self.game.n_rounds_known,
            self.game.payoff_matrix
        )
        return creator.fill_template(agent, opponents, self.round_number, self.game.history.rounds, phase)

    def _execute_agent_strategy(self, agent, prompt):
        # We handle retry at the execute_prompt level somewhat
        response = agent.execute_round(prompt)
        print(f"[{agent.name}] Response: {response}")
        found_strategy = next(
            (key for key, val in self.game.payoff_matrix.strategies.items()
             if val.lower() in response.lower()), None
        )
        if found_strategy:
            agent.add_strategy(self.game.payoff_matrix.strategies[found_strategy])
            return found_strategy
        
        # Heuristic fallback if direct match fails: check for partial match or assume first strategy
        # For robustness in experiments, we might want to default or raise
        print(f"[{agent.name}] No exact strategy match found. Defaulting to first strategy.")
        fallback = list(self.game.payoff_matrix.strategies.keys())[0]
        agent.add_strategy(self.game.payoff_matrix.strategies[fallback])
        return fallback

    def _update_round_history(self):
        for agent in self.game.agents.values():
            self.game.history.update_round(self.round_number, agent.name, {
                'strategy': agent.last_strategy(),
                'score': agent.last_score()
            })

class FairGame:
    def __init__(self, name, language, agents, n_rounds, n_rounds_known,
                 payoff_matrix_data, prompt_template, stop_conditions, agents_communicate):
        self.name = name
        self.language = language
        self.agents = agents
        self.n_rounds = int(n_rounds)
        self.n_rounds_known = n_rounds_known
        self.prompt_template = prompt_template
        self.stop_conditions = stop_conditions
        self.agents_communicate = agents_communicate
        self.current_round = 1
        self.history = GameHistory()
        self.choices_made = []
        self.payoff_matrix = PayoffMatrix(payoff_matrix_data, language)

    def run_round(self):
        runner = GameRound(self)
        round_strategies = runner.run()
        self.choices_made.append(round_strategies)
        self.payoff_matrix.attribute_scores(list(self.agents.values()), round_strategies)
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
            config.get('agentsCommunicate', False)
        )

# --- 4. EXPERIMENT SETUP (TEMPLATES & CONFIGS) ---

DEFAULT_TEMPLATE = """
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
"""

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
        "en": {"strategy1": "Contribute", "strategy2": "Keep"}
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
        # Weights map to agents [A1, A2, A3]
        "CCC": ["GlobalWin", "GlobalWin", "GlobalWin"],
        "CCD": ["Sucker", "Sucker", "FreeRide"], # 2 contributors, 1 free rider
        "CDC": ["Sucker", "FreeRide", "Sucker"],
        "DCC": ["FreeRide", "Sucker", "Sucker"],
        "CDD": ["Sucker", "FreeRide", "FreeRide"], # 1 contributor, 2 free riders
        "DCD": ["FreeRide", "Sucker", "FreeRide"],
        "DDC": ["FreeRide", "FreeRide", "Sucker"],
        "DDD": ["AllDefect", "AllDefect", "AllDefect"]
    }
}

PGG_CONFIG = {
    "name": "Public Goods Game (3-Player)",
    "nRounds": 5, # Test with 5 rounds
    "nRoundsIsKnown": True,
    "llm": "MockModel", # Change to "OpenAIGPT4o" or "Claude35Haiku"
    "languages": ["en"],
    "promptTemplate": {"en": DEFAULT_TEMPLATE},
    "agents": {
        "names": ["Alice", "Bob", "Charlie"],
        "personalities": {
            "en": ["Cooperative", "Selfish", "Tit-for-Tat"]
        },
        "opponentPersonalityProb": [100, 100, 100]
    },
    "payoffMatrix": PGG3_PAYOFF
}

# 3-Player Triadic PD Config
TRIADIC_PD_PAYOFF = {
    "weights": {
        "Reward": 7,       # CCC (All Cooperate)
        "Temptation": 9,   # D vs CC (Defector Temptation)
        "Sucker": 2,       # C vs CD (Cooperator Sucker)
        "Punishment": 1,   # DDD (All Defect)
        "LoneSucker": 0,   # C vs DD (Lone Sucker)
        "Exploiter": 5     # D vs CD (Exploiter in mixed group)
    },
    "strategies": {
        "en": {"strategy1": "Cooperate", "strategy2": "Defect"}
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
        "CDD": ["LoneSucker", "Exploiter", "Exploiter"],
        "DCD": ["Exploiter", "LoneSucker", "Exploiter"],
        "DDC": ["Exploiter", "Exploiter", "LoneSucker"],
        "DDD": ["Punishment", "Punishment", "Punishment"]
    }
}

TRIADIC_PD_CONFIG = PGG_CONFIG.copy()
TRIADIC_PD_CONFIG["name"] = "Triadic Prisoner's Dilemma"
TRIADIC_PD_CONFIG["payoffMatrix"] = TRIADIC_PD_PAYOFF

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run FAIRGAME Experiments")
    parser.add_argument("--model", type=str, default="MockModel", 
                        choices=["MockModel", "OpenAIGPT4o", "Claude35Haiku", "MistralLarge"],
                        help="LLM provider model to use")
    parser.add_argument("--rounds", type=int, default=5, help="Number of rounds")
    parser.add_argument("--game", type=str, default="PGG", choices=["PGG", "PD"], help="Game to run")
    
    args = parser.parse_args()
    
    print(f"Initializing FAIRGAME Standalone Experiment: {args.game} with {args.model} for {args.rounds} rounds...")
    
    factory = FairGameFactory()
    
    if args.game == "PD":
        config = TRIADIC_PD_CONFIG
    else:
        config = PGG_CONFIG

    # Update Config with CLI args
    config['llm'] = args.model
    config['nRounds'] = args.rounds
    
    results = factory.create_and_run_games(config)
    
    print("\n--- RESULTS ---")
    print(json.dumps(results, indent=2))
    
    # Save to file
    filename = f"experiment_results_{args.game}_{args.model}_{args.rounds}.json"
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {filename}")
