from dataclasses import dataclass

@dataclass
class StatusCondition:
    name: str
    description: str
    
    def get_prompt_description(self) -> str:
        return f"- {self.name}: {self.description}"

class StatusConditionTypes:
    # status conditions that last multiple turns
    POISONED = StatusCondition("Poisoned", "Takes small additional damage every turn, cannot be removed")
    CONFUSED = StatusCondition("Confused", "High chance to damage yourself in your confusion")
    IMMOBILE = StatusCondition("Immobile", "Cannot move your legs, can still do ranged attacks or attack someone in melee range")
    PACIFIED = StatusCondition("Pacified", "Contemplate your aggression, might not take action this turn")
    VULNERABLE = StatusCondition("Vulnerable", "Take double damage next turn")

    # status conditions that exist only for the active turn
    BLINDED = StatusCondition("Blinded", "Your actual target will not be your intended target this turn")
    STUNNED = StatusCondition("Stunned", "Unable to take any action this turn")
    WEAKENED = StatusCondition("Weakened", "Reflected in your action description, your attacks are weaker this turn")
    
    @classmethod
    def get_ongoing_status_conditions(cls) -> list[StatusCondition]:
        return [cls.POISONED, cls.CONFUSED, cls.IMMOBILE, cls.PACIFIED, cls.VULNERABLE]
    
    @classmethod
    def get_single_turn_status_conditions(cls) -> list[StatusCondition]:
        return [cls.BLINDED, cls.STUNNED, cls.WEAKENED]
    
    @classmethod
    def format_ongoing_conditions_for_prompt(cls) -> str:
        conditions = [condition.get_prompt_description() for condition in cls.get_ongoing_status_conditions()]
        return "\n".join(conditions) if conditions else "None"
    
    @classmethod
    def format_single_turn_conditions_for_prompt(cls) -> str:
        conditions = [condition.get_prompt_description() for condition in cls.get_single_turn_status_conditions()]
        return "\n".join(conditions) if conditions else "None"