import sys
import random

from dotenv import load_dotenv
from rich import print

from battle_round import BattleRound
from battler_class import BattlerClass
from llm_managers.gemini_manager import generate_response_with_fallback
from models import ContestantSchema, RosterResponse, Battler, parse_roster_response
from prompts import contestant_selection_prompt
from utils import print_with_delay

def main() -> None:
    load_dotenv()
    show_arena_introduction()

    try:
        roster = create_roster()
    except Exception as e:
        print(f"Initial setup of the arena failed: {e}")
        sys.exit(1)

    for contestant in roster:
        contestant.introduce()

    battle_loop(roster)

def show_arena_introduction() -> None:
    print_with_delay("[bold]Welcome, [italic]ladies and gentlemen[/italic], to the electrifying AI Battle Arena![/bold]")
    print_with_delay("Tonight, [bold]four legendary champions[/bold] will clash in a contest of [italic]wits, strategy, and sheer determination[/italic].")
    print_with_delay("Each battler brings a [bold]unique story[/bold], a [bold]powerful skillset[/bold], and an [bold]unbreakable will to win[/bold].")
    print_with_delay("[italic]Who will rise to glory and who will fall? The anticipation is palpable![/italic]")
    print_with_delay("Get ready to meet our [bold]fearless competitors[/bold] and witness [italic]history in the making[/italic]!")

def create_roster() -> list[ContestantSchema]:
    random_class_subset = [battler_class.value for battler_class in BattlerClass.get_random_battler_classes()]
    prompt = contestant_selection_prompt(random_class_subset)

    response = generate_response_with_fallback(
        prompt=prompt,
        response_schema=RosterResponse
    )

    return parse_roster_response(response.text)

def battle_loop(roster: list[ContestantSchema]) -> None:
    battler_roster = [Battler(**contestant.model_dump()) for contestant in roster]

    turn_order = determine_turn_order(battler_roster)
    round_number = 1
    battle_history = []

    while True:
        battle_round = BattleRound(round_number, battler_roster, battle_history)
        if len(battle_round.active_battlers) < 2:
            break

        print_with_delay(f"\n[bold yellow]--- ROUND {round_number} ---[/bold yellow]")
        battle_round.initiate_battle_round()
        round_number += 1

    if len(battle_round.active_battlers) == 1:
        winner = battle_round.active_battlers[0]
        print_with_delay(f"\n{winner.get_formatted_name_and_class()} [bold green]is the victor![/bold green]")
    else:
        print_with_delay("\n[bold red]It... it's a draw!? How did this happen?[/bold red]")

def determine_turn_order(battler_roster: list[Battler]) -> list[Battler]:
    random.shuffle(battler_roster)
    return battler_roster

if __name__ == "__main__":
    main()