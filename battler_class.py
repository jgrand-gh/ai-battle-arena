import random

from enum import Enum

class BattlerClass(Enum):
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

    def get_description(self) -> str:
        descriptions = {
            self.KNIGHT: "You are a noble warrior who can withstand heavy blows and dominate the battlefield with your sword and shield.",
            self.BERSERKER: "You are a fierce fighter who channels rage into devastating attacks, overwhelming your foes with brute strength.",
            self.MONK: "You are a disciplined martial artist who masters body and mind, striking swiftly and precisely.",
            self.NINJA: "You are a stealthy assassin who uses ninjutsu and agility to outmaneuver and eliminate enemies.",
            self.ROGUE: "You are a cunning trickster who strikes from the shadows, using deception, agility, and deadly poisons to your advantage.",
            self.RANGER: "You are a relentless marksman whose arrows strike true from any distance.",
            self.BARD: "You are a charismatic performer who confounds foes with your clever lyrics, distracting rhythms, and unpredictable tactics.",
            self.DRUID: "You are a shapeshifter who draws on the fury of beasts, transforming to unleash primal attacks.",
            self.ELEMENTALIST: "You are a wielder of elemental magic who commands fire, ice, lightning, and earth to devastate your enemies.",
            self.ILLUSIONIST: "You are a master of deception who bends reality and confuses opponents with powerful illusions.",
            self.WARLOCK: "You are a dark sorcerer who draws power from otherworldly entities to unleash forbidden magic.",
            self.NECROMANCER: "You are a sinister spellcaster who commands the dead to do your bidding.",
            self.PACIFIST: "You are a mentalist who can control emotions, solving conflicts without violence."
        }
        return descriptions[self]

    def get_actions(self) -> dict[str, str]:
        actions = {
            self.KNIGHT: {
                "Attack": "Skillful Slash",
                "Devastating Attack": "Stagger and Pierce",
                "Special Ability": "Shield Boomerang (can interrupt attacks)"
            },
            self.BERSERKER: {
                "Attack": "Axe Cleave",
                "Devastating Attack": "Reckless Charge",
                "Special Ability": "Piercing Roar (hits all targets by name)"
            },
            self.MONK: {
                "Attack": "Brutal Palm",
                "Devastating Attack": "Barrage of a Thousand Fists",
                "Special Ability": "Calming Grace (reduces target aggression)"
            },
            self.NINJA: {
                "Attack": "Shuriken Toss",
                "Devastating Attack": "Ninjutsu Assault",
                "Special Ability": "Teleportation Strike (unguardable attack)"
            },
            self.ROGUE: {
                "Attack": "Backstab",
                "Devastating Attack": "Eviscerate",
                "Special Ability": "Poisoned Blade (poisons target)"
            },
            self.RANGER: {
                "Attack": "Quick Nock",
                "Devastating Attack": "Arrow Shower",
                "Special Ability": "Bind Limbs (immobilizes target)"
            },
            self.BARD: {
                "Attack": "Discordant Song",
                "Devastating Attack": "Ear-Shattering Cacophony",
                "Special Ability": "Paralyzing Ditty (stuns target)"
            },
            self.DRUID: {
                "Attack": "Wolf Form - Bite",
                "Devastating Attack": "Bear Form - Maim and Dismember",
                "Special Ability": "Raven Form - Eye Peck (blinds target)"
            },
            self.ELEMENTALIST: {
                "Attack": "choose - Fireball / Ice Bolt / Lightning / Rock Shard",
                "Devastating Attack": "Quad-Element Devastation",
                "Special Ability": "choose - Fire Wall / Ice Cage / Shock Step / Stoneskin"
            },
            self.ILLUSIONIST: {
                "Attack": "Mind Shear",
                "Devastating Attack": "Mind Shatter",
                "Special Ability": "Delusional Affliction (confuses target)"
            },
            self.WARLOCK: {
                "Attack": "Shadow Bolt",
                "Devastating Attack": "Shadow Tendril Assault",
                "Special Ability": "Transfer Pain (redirects damage from self to another target)"
            },
            self.NECROMANCER: {
                "Attack": "Bone Toss",
                "Devastating Attack": "Dreadbone Colossus Smash",
                "Special Ability": "Skeletal Dogpile (buries target in a pile of skeletons)"
            },
            self.PACIFIST: {
                "Attack": "Calming Wave",
                "Devastating Attack": "Cerebral Override",
                "Special Ability": "Crisis of Confidence (inflicts target with crushing self-doubt)"
            }
        }
        return actions.get(self, {
            "Attack": "Basic Attack",
            "Devastating Attack": "Power Attack", 
            "Special Ability": "Class Ability"
        })

    @classmethod
    def get_random_battler_classes(cls, amount: int = 4) -> list['BattlerClass']:
        return random.sample(list(cls), amount)