from src.narrative_engine.llm.connection import Llama, Gemini
from src.narrative_engine.model.narrativeState import NarrativeState
from src.narrative_engine.model.action import Action
LANGUAGE = "Spanish"

class NarrativeGenerator:

	def __init__(
		self,
		provider: Llama | Gemini
	):
		self.llm = provider

	def describe_state(
		self,
		state: NarrativeState
	) -> str: 
		description = []
		description.append("Characters:")

		for character in state.characters.values():
			for attribute, value in character.attributes.items():
				description.append(
					f"- {character.name} is {attribute}: {value}"
				)

			for pocket, value in character.pockets.items():
				description.append(
					f"  - {character.name} habe {pocket}: {value}"
				)

		for mood, value in state.moods.items():
			description.append(
				f"The state feels {mood}: {value}"
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

	def describe_history(
		self,
		narrative_history: list[str]
	) -> str:
		description = []
		sceneNumber = 1
		for histories in narrative_history:
			description.append(f"Scene {sceneNumber}: " + histories)
			sceneNumber += 1

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
			description.append(
				f"- {character.name} attributes:"
			)
			for attribute, value in characterNStep.attributes.items():
				if character.attributes.get(attribute):
					if character.attributes.get(attribute) == value :
						status = f"{attribute} remained in {value}"

					else:
						status = f"{attribute} changed from {character.attributes.get(attribute)} to {value}"

				else:
					status = f"has a new attribute {attribute}: {value}"

				description.append(
					f"        - {status}"
				)

			for pocket, value in characterNStep.pockets.items():
				status = ""
				if pocket in character.pockets:
					valuePStep = character.pockets.get(pocket)
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
					f"  - {pocket} {status}"
				)

		if current_state.moods:
			description.append("Global moods:")

			for mood, value in current_state.moods.items():
				status = ""
				if mood in previous_state.moods:
					valuePstep = previous_state.moods.get(mood)
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
					f"  - {mood} {status}"
				)

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
		rules: str = "",
		previous_state: NarrativeState = None,
		action: Action = None,
		narrative_history: list[str] = None
	) -> str:
		prompt:str
		if previous_state is None and action is None:
			stateDescribed = self.describe_state(
				current_state
			)
			prompt = f"""
You are the narrator of an interactive story.

NARRATIVE RULES:
{rules}

NARRATIVE STATE:
{stateDescribed}

Write a short introduction of the story MUST be consistent with every fact above.

Do not explain the rules.
Do not mention the narrative state.
Do not mention the constraints.

Write only the story.

In {LANGUAGE} language.
"""
		else:
			historyPreceded = self.describe_history(
				narrative_history
			)
			transitionDescribed = self.describe_transition(
				previous_state,
				current_state,
				action
			)
			prompt = f"""
You are the narrator of an interactive story.

PREVIOUS NARRATIVE STORY:
{historyPreceded}

NARRATIVE RULES:
{rules}

NARRATIVE TRANSITION:
{transitionDescribed}

The continuation MUST be consistent with the transition.

Write a short narrative continuation.

Do not explain these rules.
Do not mention the narrative state.
Do not mention the constraints.

Write only the story.

In {LANGUAGE} language.
"""
		return self.llm.generate(prompt)