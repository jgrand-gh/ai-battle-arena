import random

from typing import Tuple
from utils import print_with_delay, staggered_print_with_delay
from prompts import battler_action_system_prompt
from roster import Battler, BattleActionResponse, parse_battle_action_response
from gemini_conversation_manager import generate_response_with_fallback

class BattleRound():
    def __init__(self, round_number, battle_roster, battle_history):
        self.round_number = round_number
        self.battle_roster = battle_roster
        self.battle_history = battle_history
        self.turn_order = {}
        self.alive_battlers = self.get_alive_battlers()

    def get_alive_battlers(self):
        return [b for b in self.battle_roster if not b.is_defeated]

    def get_available_actions(self):
        return ["Attack", "Devastating Attack (Leaves you vulnerable)", "Special Ability"]

    def determine_turn_order(self):
        self.turn_order = {}
        self.alive_battlers = self.get_alive_battlers()
        num_battlers = len(self.alive_battlers)
        rolls = random.sample(range(0, 101), num_battlers)

        for battler in self.alive_battlers:
            self.turn_order[rolls.pop()] = battler

    def initiate_battle_round(self):
        self.determine_turn_order()

        ordered: list[Tuple[int, Battler]] = sorted(self.turn_order.items(), reverse=True)
        print_with_delay(f"This round's turn order: {[b.get_formatted_name_and_class_string() for _, b in ordered]}")

        for _, battler in ordered:
            if battler.is_defeated:
                continue
            
            if len(self.alive_battlers) < 2:
                break
            
            other_alive_battlers = [b.first_name for b in self.alive_battlers if b != battler]

            system_prompt = battler_action_system_prompt(
                battler_name=battler.first_name,
                battler_class=battler.character_class.value,
                battler_pronouns=battler.pronouns,
                viable_actions=self.get_available_actions(),
                alive_battlers=other_alive_battlers
            )
            
            history_context = "\n".join(self.battle_history[-12:]) if self.battle_history else "The battle has just begun."
            prompt = f"Battle History:\n{history_context}\n\nWhat is your action?"
            
            try:
                response = generate_response_with_fallback(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    response_schema=BattleActionResponse.model_json_schema()
                )
                
                battle_action = parse_battle_action_response(response.text)
                
                print_with_delay(f"\n{battler.get_formatted_name_and_class_string()}'s turn:")
                
                if battle_action.reaction:
                    print_with_delay(f"[italic]{battle_action.reaction}[/italic]")
                    self.battle_history.append(
                        f"{battler.first_name} reacted: {battle_action.reaction}"
                    )
                
                if not battle_action.is_defeated and battle_action.action:
                    print_with_delay(f"[bold]{battle_action.action_description}[/bold]")
                    if battle_action.target:
                        print_with_delay(f"[italic]Targeting: {battle_action.target}[/italic]")
                    staggered_print_with_delay(f"{battler.get_formatted_name_string()}: {battle_action.verbal_response}")
                    
                    self.battle_history.append(
                        f"{battler.first_name} used {battle_action.action} on {battle_action.target}: {battle_action.action_description}"
                    )
                else:
                    print_with_delay(f"{battler.get_formatted_name_string()}: ", end='')
                    staggered_print_with_delay(battle_action.verbal_response, 0.5)

                    print_with_delay(f"{battler.first_name} collapses, utterly defeated.")
                    battler.is_defeated = True
                    self.battle_history.append(f"{battler.first_name} has been defeated!")

                    self.alive_battlers = self.get_alive_battlers()

            except Exception as e:
                print(f"Error processing {battler.first_name}'s turn: {e}")
                continue