from src.narrative_engine.model.narrativeState import NarrativeState

class AssembleNarrativeRules:

    def assemble(
        state: NarrativeState
    ) -> str:
        anyAttribute: bool
        anyObjectPocket: bool
        rules = []

        rules.append(
            "The narrative state is the source of truth."
        )

        rules.append(
            "Every generated event must be consistent "
            "with the current narrative state."
        )

        for character in state.characters.values():

            if character.attributes:
                rules.append(
                    f"Don´t change any value of the attributes. "
                    f"If the attribute represents a player's state,"
                     " it cannot be altered in the text; however,"
                     " if there has been a change from a previous state to the current one,"
                     " that change must be specified—though"
                     " it cannot simply be modified to match the current state."
                )

                anyAttribute = True

            if character.pockets:
                rules.append(
                    f"The contents of {character.name}'s pockets are fixed."
                )

                rules.append(
                    f"{character.name} may only use items that exist in "
                    f"{character.name}'s pockets."
                )

                anyObjectPocket = True

        if anyAttribute:
            rules.append(
                f"The narrator must not create new atributtes."
            )

        if anyObjectPocket:
            rules.append(
                f"The narrator must not create new items."
            )

        rules.append(
            f"The current location is {state.location}."
        )

        for mood, value in state.moods.items():
            rules.append(
                f"Exist a mood that represent {mood}"
            )

        if state.moods:
            rules.append(
                f"The mood is an important element of the story,"
                " as it dictates how the narrative should be told."
                " It must remain consistent throughout the writing process"
                " and should not be explicitly stated or described within the text itself;"
                " rather, it is a factor that the writer must keep in mind without making it overt in the writing."
            )

        for flag, value in state.flags.items():
            rules.append(
                f"Exist a flag that represent {flag}"
            )

        if state.flags:
            rules.append(
                f"Don´t change any value of the flags. "
                "If the name of a flag is similar to another attribute of the scenario, "
                "the attribute is treated as the primary element and the flag as an addition."
            )

        return "\n".join(
            f"- {rule}"
            for rule in rules
        )