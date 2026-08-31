from narrative_engine.llm.llama import Llama
LANGUAGE = "Spanish"

class NarrativeGenerator:

	def __init__(
		self,
		llm: Llama
	):
		self.llm = llm

	def generate(
		self,
		current_state,
		previous_state=None,
		action_name=None
	) -> str:
		prompt:str
		if previous_state is None and action_name is None:
			prompt = f"""
You are the narrator of an interactive story.

The narrative state:

{current_state}

Write a short introduction of the story based ONLY on the
narrative state.

Do not invent changes to the narrrative state.
Do not change character status, flags, location or tension.

Write only the narrative text.

In {LANGUAGE} language.
"""
		else:
			prompt = f"""
You are the narrator of an interactive story.

The player performed this action:

{action_name}

Previous narrative state:

{previous_state}

New narrative state:

{current_state}

Write a short continuation of the story based ONLY on the
changes produced by the action.

Do not invent changes to the narrrative state.
Do not change character status, flags, location or tension.

Write only the narrative text.

In {LANGUAGE} language.
"""
		return self.llm.generate(prompt)