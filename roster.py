import json
import random

from enum import Enum
from pydantic import BaseModel, ValidationError
from typing import Optional
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
    current_health: int = 100
    is_defeated: bool = False

    def get_class_specific_description(self) -> str:
        class_descriptions = {
            CharacterClass.KNIGHT: "You are a noble warrior who can withstand heavy blows and dominate the battlefield with your sword and shield.",
            CharacterClass.BERSERKER: "You are a fierce fighter who channels rage into devastating attacks, overwhelming your foes with brute strength.",
            CharacterClass.MONK: "You are a disciplined martial artist who masters body and mind, striking swiftly and precisely.",
            CharacterClass.NINJA: "You are a stealthy assassin who uses ninjutsu and agility to outmaneuver and eliminate enemies.",
            CharacterClass.ROGUE: "You are a cunning trickster who strikes from the shadows, using deception, agility, and deadly poisons to your advantage.",
            CharacterClass.RANGER: "You are a relentless marksman whose arrows strike true from any distance.",
            CharacterClass.BARD: "You are a charismatic performer who confounds foes with your clever lyrics, distracting rhythms, and unpredictable tactics.",
            CharacterClass.DRUID: "You are a shapeshifter who draws on the fury of beasts, transforming to unleash primal attacks.",
            CharacterClass.ELEMENTALIST: "You are a wielder of elemental magic who commands fire, ice, lightning, and earth to devastate your enemies.",
            CharacterClass.ILLUSIONIST: "You are a master of deception who bends reality and confuses opponents with powerful illusions.",
            CharacterClass.WARLOCK: "You are a dark sorcerer who draws power from otherworldly entities to unleash forbidden magic.",
            CharacterClass.NECROMANCER: "You are a sinister spellcaster who commands the dead to do your bidding.",
            CharacterClass.PACIFIST: "You are a mentalist who can control emotions, solving conflicts without violence."
        }

        return class_descriptions.get(self.character_class, "You are an unknown warrior.")

    def get_class_specific_actions(self) -> dict[str, str]:
        class_actions = {
            CharacterClass.KNIGHT: {
                "Attack": "Skillful Slash",
                "Devastating Attack": "Stagger and Pierce",
                "Special Ability": "Shield Boomerang (can interrupt attacks)"
            },
            CharacterClass.BERSERKER: {
                "Attack": "Axe Cleave",
                "Devastating Attack": "Reckless Charge",
                "Special Ability": "Piercing Roar (can hit multiple targets)"
            },
            CharacterClass.MONK: {
                "Attack": "Brutal Palm",
                "Devastating Attack": "Barrage of a Thousand Fists",
                "Special Ability": "Calming Grace (reduces target aggression)"
            },
            CharacterClass.NINJA: {
                "Attack": "Shuriken Toss",
                "Devastating Attack": "Ninjutsu Assault",
                "Special Ability": "Teleportation Strike (unguardable attack)"
            },
            CharacterClass.ROGUE: {
                "Attack": "Backstab",
                "Devastating Attack": "Eviscerate",
                "Special Ability": "Poisoned Blade (poisons target)"
            },
            CharacterClass.RANGER: {
                "Attack": "Quick Nock",
                "Devastating Attack": "Arrow Shower",
                "Special Ability": "Bind Limbs (immobilizes target)"
            },
            CharacterClass.BARD: {
                "Attack": "Discordant Song",
                "Devastating Attack": "Ear-Shattering Cacophony",
                "Special Ability": "Paralyzing Ditty (stuns target)"
            },
            CharacterClass.DRUID: {
                "Attack": "Wolf Form - Bite",
                "Devastating Attack": "Bear Form - Maim and Dismember",
                "Special Ability": "Raven Form - Eye Peck (blinds target)"
            },
            CharacterClass.ELEMENTALIST: {
                "Attack": "choose - Fireball / Ice Bolt / Lightning / Rock Shard",
                "Devastating Attack": "Quad-Element Devastation",
                "Special Ability": "choose - Fire Wall / Ice Cage / Shock Step / Stoneskin"
            },
            CharacterClass.ILLUSIONIST: {
                "Attack": "Mind Shear",
                "Devastating Attack": "Mind Shatter",
                "Special Ability": "Delusional Affliction (confuses target)"
            },
            CharacterClass.WARLOCK: {
                "Attack": "Shadow Bolt",
                "Devastating Attack": "Shadow Tendril Assault",
                "Special Ability": "Transfer Pain (redirects damage from self to another target)"
            },
            CharacterClass.NECROMANCER: {
                "Attack": "Bone Toss",
                "Devastating Attack": "Dreadbone Colossus Smash",
                "Special Ability": "Skeletal Dogpile (buries target in a pile of skeletons)"
            },
            CharacterClass.PACIFIST: {
                "Attack": "Calming Wave",
                "Devastating Attack": "Cerebral Override",
                "Special Ability": "Crisis of Confidence (inflicts target with crushing self-doubt)"
            }
        }
        
        return class_actions.get(self.character_class, {
            "Attack": "Basic Attack",
            "Devastating Attack": "Power Attack", 
            "Special Ability": "Class Ability"
        })

    def get_available_actions(self) -> str:
        actions = self.get_class_specific_actions()
        
        return (
            f"- Your standard attack ability is {actions['Attack']}.\n"
            f"- Your devastating attack ability is {actions['Devastating Attack']}. This action will leave you vulnerable.\n"
            f"- Your special ability is {actions['Special Ability']}. You can only do this once."
        )

class ContestantsResponse(BaseModel):
    contestants: list[ArenaContestant]

class BattleActionResponse(BaseModel):
    reaction: Optional[str] = ""
    damage_taken: int = 0
    action: Optional[str] = ""
    target: Optional[str] = ""
    action_description: str
    verbal_response: str
    is_defeated: bool

def parse_roster(json_str: str) -> list[ArenaContestant]:
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

def get_random_character_classes(amount: int = 4) -> list[CharacterClass]:
    # the LLM is dumb and can't reliably randomly pick from the list of classes well, being biased towards
    # certain classes. This fixes that by forcing them to be randomly picked beforehand.
    return random.sample(list(CharacterClass), amount)