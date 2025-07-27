def contestant_selection_prompt(available_classes: list[str]) -> str:
    return "\n".join([
        "Please choose 4 battlers to take part in a no-holds-barred battle arena.",
        f"For each battler, assign a unique character class from the available options: {', '.join(available_classes)}. Do not repeat any class.",
        "Then, generate the following for each battler:",
        "- a unique first and last name (do not use titles such as 'Sir')",
        "- a set of your designated pronouns"
        "- a brief description of the battler and what they're fighting for",
        "- a signature introductory taunt, aimed at their fellow battlers",
        "- a unique designated color",
        "Be creative and ensure each battler is distinct from the others!",
    ])

def battle_turn_system_prompt(
        battler_name: str,
        battler_class: str,
        battler_pronouns: str,
        battler_class_description: str,
        battler_health: int,
        available_actions: str,
        active_battlers: list[str],
        can_use_special: bool,
    ) -> str:
    return "\n".join ([
        f"You are {battler_name}, a {battler_class}, participating in the AI Battle Arena. Your pronouns are {battler_pronouns}.",
        f"{battler_class_description}",
        f"Your goal is to be the last battler standing, and to eliminate everyone else. You are currently at {battler_health} / 100 health.",
        "Your available actions (choose one):",
        f"\n{available_actions}\n",
        f"Your special ability is {'available to be used' if can_use_special else 'not available to be used'}.",
        f"Active battlers: {', '.join(active_battlers)}. If there's only one other battler, focus on ending the battle at all costs.",
        "Generate the following in your response (use third person for your action/reaction descriptions and don't exceed 50 words for each):",
        "",
        "- a reaction to any recent actions that targeted you, ONLY if you've not already reacted to the actions (disregard entirely if there weren't any)",
        "More specifically, describe how the action connected with you and the damage you took from it. Be realistic, don't just act as though you can shrug off every attack.",
        "If the action was enough to kill or incapacitate you, do not provide a subsequent action or target.",
        "- the amount of damage taken from the last action, if applicable. Physical, mental or emotional damage are all valid.",
        "If this reduces your health to 0 or below, then I'm sorry, you have been defeated.",
        "- an action you are taking, and the target with which you'd like to take the action at",
        "- a brief description of the action, described as though it is 'in-motion'",
        "The target will respond accordingly as to how the attack connects with them.",
        "- a verbal response for your action, such as taunting or shouting, or expressing pain as you are defeated",
        "Do not describe how you're saying it, just what you're saying.",
        "- an indication if you've used your special ability this turn",
        "",
        "Consider your character's personality and current situation when choosing your action.",
        "You will be provided with a message history describing the events of the battle so far. Use this context to inform your next action.",
    ])