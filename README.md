# AI Battle Arena

AI Battle Arena is a Python-based simulation platform where AI contestants, powered by large language models (LLMs), compete in a turn-based battle environment. The project is designed for experimentation with prompt engineering, LLM strategies, and interactive AI competitions.

## Features

- Run simulated battles between AI contestants using Google Gemini
- Modular contestant system for easy addition of new AI agents
- Configurable battle rounds and rules
- Command-line interface for running and observing battles

> **Note:** The OpenRouter LLM interface is currently defunct and should not be used.

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

## Project Structure

- `main.py` — Entry point, runs the battle arena simulation
- `llm_managers/` — LLM interaction managers (e.g., `gemini_manager.py`)
- `models.py` — Contestant and battler models, response schemas, and parsing logic
- `battler_class.py` — Enum and logic for battler classes, descriptions, and actions
- `roster.py` — Roster creation and contestant management
- `battle_round.py` — Handles the logic for each round of the battle
- `prompts.py` — Contains prompt templates for LLMs
- `utils.py` — Utility functions for printing and formatting
- `requirements.txt` — Python dependencies
- `.env` — API keys and configuration (not committed)

## License

This project is a submission to the Boot.dev 2025 Hackathon.