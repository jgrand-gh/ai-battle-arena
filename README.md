# AI Battle Arena

AI Battle Arena is a Python-based simulation platform where AI contestants, powered by large language models (LLMs), compete in a turn-based battle environment. The project is designed for experimentation with prompt engineering, LLM strategies, and interactive AI competitions.

This project was designed with the inherent goal of letting the LLMs dictate the flow of combat. As a result, this often leads to scenarios where the AI contestants will 100% break the rules and defy all odds, but hey, that's technically what they're allowed to do.

This project is a submission to the [Boot.dev](https://boot.dev) 2025 Hackathon.

> **Note:** The original plan was to leverage OpenRouter's interface to have each AI contestant controlled by a separate LLM, but as the scope of this project was within a hackathon, it was easier (and free) to use Google Gemini for all of the contestants instead.

## Features

- Run simulated battles between AI contestants using Google Gemini
- 13 unique character classes with distinct abilities and special moves
- Dynamic status condition system (poisoned, confused, stunned, immobile, etc.)
- Rich console output with colored text and realistic timing effects
- Turn-based combat with reaction and action phases
- AI-generated victory speeches and character introductions
- Configurable battle rounds with comprehensive battle history tracking
- Command-line interface for running and observing battles

> **Note:** The OpenRouter LLM interface is currently defunct (and untested) and should not be used.

## Requirements

- Python 3.12 or newer
- API key for Google Gemini (set in `.env`)
- Dependencies listed in `requirements.txt`

## Getting Started

1. **Clone the repository**
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up your `.env` file** with the required API key(s):
   - For Google Gemini, add the following line to your `.env` file:
     ```
     GEMINI_API_KEY="your-gemini-api-key-here"
     ```
   > A free Google AI Studio Gemini API key can be generated here: https://aistudio.google.com/apikey
   - *(Optional)* For OpenRouter (currently unsupported), you would use:
     ```
     OPENROUTER_API_KEY="your-openrouter-api-key-here"
     ```
4. **Run the main program:**
   ```sh
   python main.py
   ```

> **Tip:** You can adjust the text output speed by modifying the `DELAY_PER_WORD` constant in `utils.py`. Lower values make text appear faster, higher values slower.

## Project Structure

- `main.py` — Entry point, runs the battle arena simulation
- `llm_managers/` — LLM interaction managers
  - `gemini_manager.py` — Google Gemini API integration
  - `openrouter_manager.py` — OpenRouter API (deprecated)
- `models.py` — Contestant and battler models, response schemas, and parsing logic
- `battler_class.py` — Enum and logic for battler classes, descriptions, and actions
- `battle_round.py` — Handles the logic for each round of the battle
- `status_condition.py` — Status condition system and effects
- `prompts.py` — Contains prompt templates for LLMs
- `utils.py` — Utility functions for printing and formatting
- `requirements.txt` — Python dependencies
- `.env` — API keys and configuration (not committed)

## How It Works

1. **Roster Creation**: The system randomly selects 4 character classes and uses AI to generate unique contestants with names, descriptions, and personalities.
2. **Battle Simulation**: Contestants take turns using their class-specific abilities, with AI determining their actions and reactions based on battle context and character personalities.
3. **Status Effects**: Battlers can be affected by various conditions like poisoned, confused, or stunned, adding strategic depth.
4. **Victory**: The last battler standing gives an AI-generated victory speech.