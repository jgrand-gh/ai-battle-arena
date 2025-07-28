from models import Battler
from status_condition import StatusConditionTypes

def contestant_selection_prompt(available_classes: list[str]) -> str:
    return "\n".join([
        "Please choose 4 battlers to take part in a no-holds-barred battle arena.",
        f"For each battler, assign a unique character class from the available options: {', '.join(available_classes)}. Do not repeat any class.",
        "Then, generate the following for each battler:",
        "- a unique first and last name (do not use titles such as 'Sir')",
        "- a set of your designated pronouns"
        "- a brief description of the battler and what they're fighting for",
        "- a signature introductory taunt, aimed at their fellow battlers",
        "- a unique designated color (choose only BRIGHT colors)",
        "Be creative and ensure each battler is distinct from the others!",
    ])

def battle_turn_system_prompt(battler: Battler, active_battlers: list[str]) -> str:
    if battler.ongoing_status_conditions:
        conditions_text = f"You are currently affected by: {', '.join(battler.ongoing_status_conditions)}."
    else:
        conditions_text = "You are not currently affected by any ongoing conditions."
    
    return "\n".join([
        f"You are {battler.first_name}, a {battler.battler_class.value}, participating in the AI Battle Arena. Your pronouns are {battler.pronouns}.",
        f"{battler.get_battler_class_description()}",
        f"Your goal is to be the last battler standing, and to eliminate everyone else. You are currently at {battler.current_health} / {battler.MAX_HP} health.",
        conditions_text,
        "",
        "Your available actions (choose one):",
        f"{battler.format_actions_for_system_prompt()}",
        f"Your special ability is{' not ' if not battler.can_use_special else ' '}available to be used.",
        "",
        "You might be under the effect of a status condition this turn, consider the following:",
        "Ongoing Status Conditions (chance to remove each turn):",
        f"{StatusConditionTypes.format_ongoing_conditions_for_prompt()}",
        "Single Turn Status Conditions (only active this turn):",
        f"{StatusConditionTypes.format_single_turn_conditions_for_prompt()}",
        "You can not avoid single turn status conditions from landing, or ongoing status conditions when they're first applied.",
        "",
        f"Active battlers: {', '.join(active_battlers)}. If there's only one other battler, focus on ending the battle at all costs.",
        "",
        "Generate the following in your response (use third person for your action/reaction descriptions and don't exceed 50 words for each):",
        "- a reaction to any recent actions that targeted you, ONLY if you've not already reacted to the actions (disregard entirely if there weren't any)",
        "More specifically, describe how the action connected with you and the damage you took from it. Be realistic, don't just act as though you can shrug off every attack.",
        "If the action was enough to defeat, incapacitate or otherwise restrict your actions, do not provide a subsequent action or target.",
        "- the amount of damage taken from the last action, if applicable. Physical, mental, emotional and psychic damage are all valid forms of damage.",
        "Everything will reduce your health, at least a little. If this reduces your current health to 0 or below, then you have been defeated.",
        "- an action you are taking, and the target with which you'd like to take the action at",
        "- a brief description of the action, described as though it is 'in-motion'",
        "The target will respond accordingly as to how the attack connects with them.",
        "- a verbal response for your action, such as taunting or shouting, or expressing pain as you are defeated",
        "Do not describe how you're saying it, just what you're saying.",
        "- an indication if you've used your special ability this turn",
        "- any ongoing conditions that might be affecting you beyond this turn",
        "",
        "Consider your character's personality and current situation when choosing your action.",
        "You will be provided with a message history describing the events of the battle so far. Use this context to inform your next action.",
    ])

def victory_system_prompt(battler: Battler, other_battlers: list[str]) -> str:
    return "\n".join([
        f"You are {battler.first_name} {battler.last_name} the {battler.battler_class.value}, and you are the victor of the AI Battle Arena.",
        f"You are: {battler.description}",
        f"You have defeated all the other battlers: {', '.join(other_battlers)}.",
        "Reflect on your journey and the battles you fought to achieve this victory.",
        "Consider what this victory means for you and your future in the arena.",
        "Feel free to share any final thoughts or reflections on your experience.",
        "Keep your response around or below 200 words.",
        "The provided prompt will show the history of the final actions in the battle that led to your victory.",
    ])