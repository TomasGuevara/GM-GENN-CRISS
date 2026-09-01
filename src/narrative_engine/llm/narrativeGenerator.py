from src.narrative_engine.llm.llama import Llama
from src.narrative_engine.model.narrativeState import NarrativeState
from src.narrative_engine.model.action import Action
LANGUAGE = "Spanish"

class NarrativeGenerator:

	def __init__(
		self,
		llm: Llama
	):
		self.llm = llm

	def describe_state(
		self,
		state: NarrativeState
	) -> str: 
		description = []
		description.append("Characters:")

		for character in state.characters.values():
			status = "alive" if character.alive else "dead"
			description.append(
				f"- {character.name}: {status}"
			)

			for flag, value in character.flags.items():
				description.append(
					f"  - {flag}: {value}"
				)

		description.append(
			f"Tension: {state.tension}"
		)

		description.append(
			f"Location: {state.location}"
		)

		if state.flags:
			description.append("Global flags:")

			for flag, value in state.flags.items():
				description.append(
					f"- {flag}: {value}"
				)

		return "\n".join(description)

	def describe_transition(
		self,
		previous_state: NarrativeState,
		current_state: NarrativeState,
		action: Action
	) -> str:
		description = []
		status: str
		description.append("The player performed the action: " + action.name)

		for character in previous_state.characters.values():
			characterNStep = current_state.characters.get(character.name)
			if character.alive == characterNStep.alive :
				if character.alive:
					status = "remained alive"
				else:
					status = "remained dead"

			elif character.alive and not characterNStep.alive:
				status = "now is dead"

			else:
				status = "changed from dead to alive"

			description.append(
				f"- {character.name}: {status}"
			)

			for flag, value in characterNStep.flags.items():
				status = ""
				if flag in character.flags:
					valuePStep = character.flags.get(flag)
					if value == valuePStep:
						status = f"remained {valuePStep}"
					else:
						if isinstance(value, float):
							if value < valuePStep:
								status = f"increased from {value} to {valuePStep}"
							else:
								status = f"decreased from {value} to {valuePStep}"
						else:
							status = f"changed from {value} to {valuePStep}"
				else:
					status = f"{value}"
				
				description.append(
					f"  - {flag} {status}"
				)

		if previous_state.tension < current_state.tension:
			description.append(f"Tension increased from {previous_state.tension} to {current_state.tension}")
		elif previous_state.tension > current_state.tension:
			description.append(f"Tension decreased from {previous_state.tension} to {current_state.tension}")
		elif previous_state.tension == current_state.tension:
			description.append(f"Tension remained in {current_state.tension}")

		if previous_state.location != current_state.location:
			description.append(
				f"Location change from {previous_state.location} to {current_state.location}"
			)
		else:
			description.append(
				f"Location remained in {current_state.location}"
			)

		if current_state.flags:
			description.append("Global flags:")

			for flag, value in current_state.flags.items():
				status = ""
				if flag in previous_state.flags:
					valuePstep = previous_state.flags.get(flag)
					if value == valuePstep:
						status = f"remained {valuePstep}"
					else:
						if isinstance(value, float):
							if valuePstep < value:
								status = f"increased from {valuePstep} to {value}"
							else:
								status = f"decreased from {valuePstep} to {value}"
						else:
							status = f"changed from {valuePstep} to {value}"
				else:
					status = f"{value}"

				description.append(
					f"  - {flag} {status}"
				)

		return "\n".join(description)

	def generate(
		self,
		current_state: NarrativeState,
		previous_state: NarrativeState = None,
		action: Action = None
	) -> str:
		prompt:str
		if previous_state is None and action_name is None:
			stateDescribed = self.describe_state(
				current_state
			)
			prompt = f"""
You are the narrator of an interactive story.

The narrative state:

{stateDescribed}

Write a short introduction of the story based ONLY on the
narrative state.

Do not invent changes to the narrrative state.
Do not change character status, flags, location or tension.

Write only the narrative text.

In {LANGUAGE} language.
"""
		else:
			transitionDescribed = self.describe_transition(
				previous_state,
				current_state,
				action
			)
			prompt = f"""
You are the narrator of an interactive story.

{transitionDescribed}

Write a short continuation of the story based ONLY on the
changes produced by the action.

Do not invent changes to the narrrative state.
Do not change character status, flags, location or tension.

Write only the narrative text.

In {LANGUAGE} language.
"""
		return self.llm.generate(prompt)