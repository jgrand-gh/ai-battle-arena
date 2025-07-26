import json
import random

from enum import Enum
from pydantic import BaseModel, ValidationError
from typing import List, Optional
from utils import print_with_delay, staggered_print_with_delay

class CharacterClass(Enum):
    KNIGHT = "Knight"
    BERSERKER = "Berserker"
    MONK = "Monk"
    NINJA = "Ninja"
    ROGUE = "Rogue"
    RANGER = "Ranger"
    BARD = "Bard"
    DRUID = "Druid"
    ELEMENTALIST = "Elementalist"
    ILLUSIONIST = "Illusionist"
    WARLOCK = "Warlock"
    NECROMANCER = "Necromancer"
    PACIFIST = "Pacifist"

class ColorList(Enum):
    BRIGHT_RED = "bright_red"
    BRIGHT_GREEN = "bright_green"
    BRIGHT_YELLOW = "bright_yellow"
    BRIGHT_BLUE = "bright_blue"
    BRIGHT_MAGENTA = "bright_magenta"
    BRIGHT_CYAN = "bright_cyan"

class ArenaContestant(BaseModel):
    first_name: str
    last_name: str
    pronouns: str
    character_class: CharacterClass
    description: str
    intro_taunt: str
    text_color: ColorList

    def get_formatted_name_string(self):
        return f"[bold {self.text_color.value}]{self.first_name}[/bold {self.text_color.value}]"
    
    def get_formatted_name_and_class_string(self):
        return f"[bold][{self.text_color.value}]{self.first_name}[/bold] ({self.character_class.value})[/{self.text_color.value}]"

    def display_introduction(self):
        print_with_delay(f"\n[italic]In this corner, we have...[/italic]")
        print_with_delay(
            f"[bold][{self.text_color.value}]{self.first_name} {self.last_name}[/bold] "
            f"the [italic]{self.character_class.value}[/italic][/{self.text_color.value}]! "
            f"{self.description}"
        )
        print_with_delay(f"{self.get_formatted_name_string()}: ", end='')
        staggered_print_with_delay(f"{self.intro_taunt}")

class Battler(ArenaContestant):
    is_defeated: bool = False

class ContestantsResponse(BaseModel):
    contestants: List[ArenaContestant]

class BattleActionResponse(BaseModel):
    reaction: Optional[str] = ""
    action: Optional[str] = ""
    target: Optional[str] = ""
    action_description: str
    verbal_response: str
    is_defeated: bool

def parse_roster(json_str: str) -> List[ArenaContestant]:
    try:
        data = json.loads(json_str)
        response = ContestantsResponse(**data)
        return response.contestants
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Error parsing JSON: {e}")
        return []

def parse_battle_action_response(json_str: str) -> BattleActionResponse:
    try:
        data = json.loads(json_str)
        return BattleActionResponse(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Error parsing BattleActionResponse: {e}")
        raise

def get_random_character_classes(amount: int = 4) -> List[CharacterClass]:
    # the LLM is dumb and can't reliably randomly pick from the list of classes well, being biased towards
    # certain classes. This fixes that by forcing them to be randomly picked beforehand.
    return random.sample(list(CharacterClass), amount)