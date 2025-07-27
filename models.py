import json

from pydantic import BaseModel, ValidationError
from typing import Optional

from battler_class import BattlerClass
from utils import ColorList, print_with_delay, staggered_print_with_delay

class ContestantSchema(BaseModel):
    first_name: str
    last_name: str
    pronouns: str
    battler_class: BattlerClass
    description: str
    intro_taunt: str
    text_color: ColorList

    def get_formatted_name(self) -> str:
        return f"[bold {self.text_color.value}]{self.first_name}[/bold {self.text_color.value}]"

    def get_name_and_class(self) -> str:
        return f"{self.first_name} ({self.battler_class.value})"

    def get_formatted_name_and_class(self) -> str:
        return f"[bold][{self.text_color.value}]{self.first_name}[/bold] ({self.battler_class.value})[/{self.text_color.value}]"

    def introduce(self):
        print_with_delay(f"\n[italic]In this corner, we have...[/italic]")
        print_with_delay(
            f"[bold][{self.text_color.value}]{self.first_name} {self.last_name}[/bold] "
            f"the [italic]{self.battler_class.value}[/italic][/{self.text_color.value}]! "
            f"{self.description}"
        )
        print_with_delay(f"{self.get_formatted_name()}: ", end='')
        staggered_print_with_delay(f"{self.intro_taunt}")

class Battler(ContestantSchema):
    current_health: int = 100
    is_defeated: bool = False
    can_use_special: bool = True

    def take_damage(self, damage: int) -> None:
        self.current_health = max(0, self.current_health - damage)
        if self.current_health <= 0:
            self.is_defeated = True

    def get_battler_class_description(self) -> str:
        return self.battler_class.get_description()

    def get_battler_class_actions(self) -> dict[str, str]:
        return self.battler_class.get_actions()

    def format_actions_for_system_prompt(self) -> str:
        actions = self.get_battler_class_actions()

        return (
            f"- Your standard attack ability is {actions['Attack']}.\n"
            f"- Your devastating attack ability is {actions['Devastating Attack']}. This action will leave you vulnerable.\n"
            f"- Your special ability is {actions['Special Ability']}. You can only do this once."
        )

class RosterResponse(BaseModel):
    contestants: list[ContestantSchema]

class BattleTurnResponse(BaseModel):
    reaction: Optional[str] = ""
    damage_taken: int = 0
    action: Optional[str] = ""
    target: Optional[str] = ""
    action_description: str
    verbal_response: str
    special_ability_used: bool = False

def parse_roster_response(json_str: str) -> list[ContestantSchema]:
    try:
        data = json.loads(json_str)
        response = RosterResponse(**data)
        return response.contestants
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format for RosterResponse: {e}")
        raise
    except ValidationError as e:
        print(f"Invalid data structure for RosterResponse: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error parsing RosterResponse: {e}")
        raise

def parse_battle_turn_response(json_str: str) -> BattleTurnResponse:
    try:
        data = json.loads(json_str)
        return BattleTurnResponse(**data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON format for BattleTurnResponse: {e}")
        raise
    except ValidationError as e:
        print(f"Invalid data structure for BattleTurnResponse: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error parsing BattleTurnResponse: {e}")
        raise