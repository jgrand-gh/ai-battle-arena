import random

from rich import print
from dotenv import load_dotenv

from roster import ContestantsResponse, ArenaContestant, Battler, parse_roster, get_random_character_classes
from gemini_conversation_manager import generate_response_with_fallback
from prompts import battler_selection_system_prompt
from utils import print_with_delay
from battle_round import BattleRound

def battle_arena_introduction():
    print_with_delay("[bold]Welcome, [italic]ladies and gentlemen[/italic], to the electrifying AI Battle Arena![/bold]")
    print_with_delay("Tonight, [bold]four legendary champions[/bold] will clash in a contest of [italic]wits, strategy, and sheer determination[/italic].")
    print_with_delay("Each battler brings a [bold]unique story[/bold], a [bold]powerful skillset[/bold], and an [bold]unbreakable will to win[/bold].")
    print_with_delay("[italic]Who will rise to glory and who will fall? The anticipation is palpable![/italic]")
    print_with_delay("Get ready to meet our [bold]fearless competitors[/bold] and witness [italic]history in the making[/italic]!")

def create_battle_roster() -> list:
    filtered_classes = [c.value for c in get_random_character_classes()]
    
    prompt = battler_selection_system_prompt(filtered_classes)
    
    response = generate_response_with_fallback(
        prompt=prompt,
        response_schema=ContestantsResponse
    )
    
    return parse_roster(response.text)

def determine_turn_order(roster):
    num_battlers = len(roster)
    rolls = random.sample(range(0, 101), num_battlers)
    turn_order = {}
    for battler in roster:
        turn_order[rolls.pop()] = battler

    return turn_order

def battle_loop(roster):
    # cast to ArenaContestant roster to Battlers
    battle_roster = [Battler(**c.model_dump()) for c in roster]

    turn_order = determine_turn_order(battle_roster)

    round_number = 1
    battle_history = []

    while True:
        active_battlers = [b for b in battle_roster if not b.is_defeated]
        if len(active_battlers) < 2:
            break

        print_with_delay(f"\n[bold yellow]--- ROUND {round_number} ---[/bold yellow]")
        round_instance = BattleRound(round_number, battle_roster, battle_history, turn_order)
        round_instance.initiate_battle_round()
        round_number += 1

    if len(active_battlers) == 1:
        winner = active_battlers[0]
        print_with_delay(f"\n{winner.get_formatted_name_string()} [bold green]is the victor![/bold green]")
    else:
        print_with_delay("\n[bold red]It... it's a draw!? How did this happen?[/bold red]")

def main():
    load_dotenv()

    battle_arena_introduction()

    try:
        roster: list[ArenaContestant] = create_battle_roster()

        for battler in roster:
            battler.display_introduction()
    except Exception as e:
        print(f"Battle setup failed: {e}")
        raise

    battle_loop(roster)

if __name__ == "__main__":
    main()