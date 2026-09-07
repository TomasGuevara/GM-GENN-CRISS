from src.narrative_engine.model.narrativeState import NarrativeState

class AssembleNarrativeRules:

    def assemble(
        state: NarrativeState
    ) -> str:
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

            if not character.alive:
                rules.append(
                    f"{character.name} is dead and "
                    "must not be described as alive."
                )

            else:
                rules.append(
                    f"{character.name} is alive and "
                    "must not be described as dead."
                )

            if character.flags:
                rules.append(
                    f"Don´t change any value of the flags. "
                    f"If the name of a flag is similar to another attribute of the character {character.name}, "
                    "the attribute is treated as the primary element and the flag as an addition."
                )

            if character.pockets:
                rules.append(
                    f"The contents of {character.name}'s pockets are fixed."
                )

                rules.append(
                    f"{character.name} may only use items that exist in "
                    f"{character.name}'s pockets."
                )

                anyObjectPocket = True

        if anyObjectPocket:
            rules.append(
                f"The narrator must not create new items."
            )

        rules.append(
            f"The current location is {state.location}."
        )

        rules.append(
            f"The current tension is {state.tension}."
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