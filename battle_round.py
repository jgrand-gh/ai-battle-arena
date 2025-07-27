from llm_managers.gemini_manager import generate_response_with_fallback
from models import BattleTurnResponse, Battler, parse_battle_turn_response
from prompts import battle_turn_system_prompt
from utils import DELAY_PER_WORD, print_with_delay, staggered_print_with_delay

class BattleRound():
    def __init__(
            self,
            round_number: int,
            battler_roster: list[Battler],
            battle_history: list[str],
        ):
        self.round_number = round_number
        self.battler_roster = battler_roster
        self.battle_history = battle_history

    @property
    def active_battlers(self) -> list[Battler]:
        return [battler for battler in self.battler_roster if not battler.is_defeated]

    def initiate_battle_round(self) -> None:
        print_with_delay(f"Turn order: {[b.get_formatted_name_and_class() for b in self.active_battlers]}")

        for battler in self.active_battlers:
            if len(self.active_battlers) < 2:
                break

            self._process_battler_turn(battler)

    def _process_battler_turn(self, battler: Battler) -> None:
            other_alive_battlers = [b.get_name_and_class() for b in self.active_battlers if b != battler]
            
            try:
                battle_action = self._get_battle_action(battler, self._generate_battler_action_system_prompt(battler, other_alive_battlers))
            except Exception as e:
                print_with_delay(f"{battler.get_formatted_name_and_class()} is mysteriously unable to act this round!")
                print(f"Error: {e}")
                return
            
            print_with_delay(f"\n{battler.get_formatted_name_and_class()}'s turn:")
            if battle_action.reaction:
                self._handle_battler_reaction(battler, battle_action)

            if battler.is_defeated:
                self._handle_battler_defeat(battler, battle_action)
            elif battle_action.action:
                self._handle_battler_action(battler, battle_action)

    def _generate_battler_action_system_prompt(self, battler: Battler, other_active_battlers: list[str]) -> str:
        return battle_turn_system_prompt(
                battler_name=battler.first_name,
                battler_class=battler.battler_class.value,
                battler_pronouns=battler.pronouns,
                battler_class_description= battler.get_battler_class_description(),
                battler_health=battler.current_health,
                available_actions=battler.format_actions_for_system_prompt(),
                active_battlers=other_active_battlers,
                can_use_special=battler.can_use_special,
            )
    
    def _get_battle_action(self, battler: Battler, system_prompt: str) -> BattleTurnResponse:
        history_context = "\n".join(self.battle_history[-12:]) if self.battle_history else "The battle has just begun."
        prompt = f"Battle History:\n{history_context}\n\nWhat is your action?"
        
        try:
            response = generate_response_with_fallback(
                prompt=prompt,
                system_prompt=system_prompt,
                response_schema=BattleTurnResponse.model_json_schema()
            )
            
            battle_action = parse_battle_turn_response(response.text)
            battler.take_damage(battle_action.damage_taken)
            if battle_action.special_ability_used:
                battler.can_use_special = False

            return battle_action
        except Exception as e:
            print(f"Error occurred while getting battle action for {battler.get_formatted_name_and_class()}: {e}")
            return BattleTurnResponse(
                action_description=f"{battler.first_name} is too confused to act!",
                verbal_response="I... I can't think straight!",
            )

    def _handle_battler_reaction(self, battler: Battler, battle_action: BattleTurnResponse) -> None:
        self.battle_history.append(f"{battler.get_name_and_class()} reacted: {battle_action.reaction}")
        print_with_delay(f"[italic]{battle_action.reaction}[/italic]")

    def _handle_battler_defeat(self, battler: Battler, battle_action: BattleTurnResponse) -> None:
        self.battle_history.append(f"{battler.first_name} has been defeated!")
        print_with_delay(f"{battler.first_name} collapses, utterly defeated.")
        print_with_delay(f"{battler.get_formatted_name()}: ", end='')
        staggered_print_with_delay(battle_action.verbal_response, DELAY_PER_WORD * 3)

    def _handle_battler_action(self, battler: Battler, battle_action: BattleTurnResponse) -> None:
        self.battle_history.append(f"{battler.first_name} used {battle_action.action} on {battle_action.target}: {battle_action.action_description}")
        print_with_delay(f"[bold]{battle_action.action_description}[/bold]")
        if battle_action.target:
            print_with_delay(f"[italic]Targeting: {battle_action.target}[/italic]")
        staggered_print_with_delay(f"{battler.get_formatted_name()}: {battle_action.verbal_response}")