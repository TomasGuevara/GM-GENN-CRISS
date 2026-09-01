import operator
import networkx as nx
from pydantic import BaseModel, Field
from src.narrative_engine.enum.operation import Operation
from src.narrative_engine.model.narrativeState import NarrativeState
from src.narrative_engine.model.condition import Condition, ConditionAnd, ConditionOr
from src.narrative_engine.model.action import Action
from src.narrative_engine.graph.narrativeGraph import NarrativeGraph
from src.narrative_engine.llm.llama import Llama
from src.narrative_engine.llm.narrativeGenerator import NarrativeGenerator

LIMIT_DEPHT = 3
GM_GENN_CRISS_VERSION = "1.0"
llama = Llama("llama3.1:8b")
generator = NarrativeGenerator(llama)

def expand_state(
	graph: NarrativeGraph,
	state_id: int,
	actions: list[Action]
):
	state = graph.get_state(state_id)

	available_actions = get_available_action(
		state,
		actions
	)

	new_state_ids = []

	for action in available_actions:
		new_state = apply_action(
			state,
			action
		)

		target_id = graph.add_state(new_state)

		graph.add_transition(
			state_id,
			target_id,
			action
		)

		new_state_ids.append(target_id)

	return new_state_ids

def validate_get_action(
	actions: [Action],
	name: str
) -> tuple[bool, Action]:
	for action in actions:

		if name == action.name:
			return True, action

	return False, None

def calculate(
	current_value: float | bool | str,
	self,
	effect_value: float | bool | str
) -> float | bool | str:

	if self == Operation.SET:
		return effect_value

	elif self == Operation.INCREMENT:
		return current_value + effect_value
    
	elif self == Operation.DECREMENT:
		return current_value - effect_value
    
	else:
		raise ValueError(f"Operación desconocida: {self}")

def get_value(
	state: NarrativeState,
	path: str
):
	parts = path.split(".")

	current = state

	for i, part in enumerate(parts):
		if isinstance(current, dict):
			if part in current:
				current = current[part]

			else:
				if i >= 1 and parts[i-1] == "flags":
					return False

				raise ValueError(
					f"No existe el atributo '{part}' en el path '{path}'"
				)

		else:
			current = getattr(current, part)

	return current

def set_value(
	state: NarrativeState,
	path: str,
	operation: Operation,
	value: float | bool | str
):
	parts = path.split(".")

	current = state

	value = calculate(get_value(state, path), operation, value)

	for part in parts[:-1]:
		if isinstance(current, dict):
			current =current[part]

		else:
			current = getattr(current, part)

	last_part = parts[-1]

	if isinstance(current, dict):
		current[last_part] = value

	else:
		setattr(current, last_part, value)

def check_preconditions(
    state: NarrativeState,
    preconditions: Condition|ConditionAnd|ConditionOr
) -> bool:
	if (isinstance(preconditions, Condition)):

		current_value = get_value(
			state,
			preconditions.path
		)

		comparator = operator.methodcaller(preconditions.operator, preconditions.value)

		if not comparator(current_value):
			return False

	elif isinstance(preconditions, ConditionOr):
		return any(
			check_preconditions(
				state,
				conditional
			)
			for conditional in preconditions.conditions
		)

	elif isinstance(preconditions, ConditionAnd):
		return all(
			check_preconditions(
				state,
				conditional
			)
			for conditional in preconditions.conditions
		)

	return True


def apply_action(
	state: NarrativeState,
	action: Action
) -> NarrativeState:

	new_state = state.model_copy(deep=True)

	if not check_preconditions(new_state, action.preconditions):
		raise ValueError(
			"La acción no cumple sus precondiciones"
		)

	for effect in action.effects:

		set_value(
			new_state,
			effect.path,
			effect.operation,
			effect.value
		)

	return new_state

def get_available_action(
	current_state: NarrativeState,
	actions: list[Action]
) -> list[Action]:
	action_list = []

	for action in actions:
		try:
			success = check_preconditions(current_state, action.preconditions)
		except ValueError as error:
			success = False

		if success:
			action_list.append(action)

	return action_list

def narrative_dfs(
	state_id: int,
	graph: NarrativeGraph,
	actions: list[Action],
	visited: set[int],
	current_depth: int
):
	if current_depth == LIMIT_DEPHT:
		return

	if state_id in visited:
		return

	visited.add(state_id)

	leaves = expand_state(
		graph,
		state_id,
		actions
	)

	for leave in leaves:
		narrative_dfs(
			leave,
			graph,
			actions,
			visited,
			current_depth+1
		)

	visited.remove(state_id)

def navigate(
	state: NarrativeState,
	graph: NarrativeGraph,
	actions: list[Action]
):
	current_state = state
	user_input = ""
	action_list: list[Action]
	success:bool
	story:str
	selected_action: Action

	print("Welcome to GM-GENN-CRISS " + GM_GENN_CRISS_VERSION)
	print("\nThe story do you live next, start like this.")
	story = generator.generate(
		current_state
	)
	print("\n"+story)

	while user_input != "Close system":
		initial_id = graph.add_state(current_state)

		narrative_dfs(
			initial_id,
			graph,
			actions,
			set(),
			0
		)

		action_list = get_available_action(
			current_state,
			actions
		)

		for action in action_list:
			print("\n" + action.name)

		print("\nClose system")
		user_input = input("\nYour decision is ")

		if user_input != "Close system":
			success, selected_action = validate_get_action(action_list, user_input)
			
			if success:
				state = current_state
				current_state = apply_action(state, selected_action)
				print("\n And the story continue like this")
				
				story = generator.generate(
    				state,
				    current_state,
    				selected_action
				)
				print("\n"+story)

				print("\n\nBehind Narrative")
				print("\nNodes")
				for node, data in graph.graph.nodes(data=True):
					print(
					"S" + str(node),
					"-->",
					data["state"]
				)

				print("\nTransitions")

				for source, target, data in graph.graph.edges(data=True):
					print(
						"S" + str(source),
						"--",
						data["action"].name,
						"-->",
						"S" + str(target)
    				)

				print("\n\nYou can do the next actions")

			else:
				print("\nThe action selected doesn't exist in the actions list mentioned.")
				print("\nWould you write one of the next options?")

	print("\nThank you for use GM-GENN-CRISS " + GM_GENN_CRISS_VERSION + ", have a nice day")