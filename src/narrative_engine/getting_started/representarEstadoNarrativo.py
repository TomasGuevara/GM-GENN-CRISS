import operator
import networkx as nx
from pydantic import BaseModel
from operation import Operation
from comparison import Comparison
from narrativeGraph import NarrativeGraph

LIMIT_DEPHT = 3

class Character(BaseModel):
    name: str
    alive: bool = True


class NarrativeState(BaseModel):
    characters: dict[str, Character]
    tension: float


class Condition(BaseModel):
    path: str
    operator: Comparison
    value: float | bool


class Effect(BaseModel):
	path: str
	operation: Operation
	value: float | bool


class Action(BaseModel):
	name: str
	preconditions: list[Condition]
	effects: list[Effect]

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
	current_value: float | bool,
	self,
	effect_value: float | bool
) -> float | bool:

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

	for part in parts:
		if isinstance(current, dict):
			current = current[part]

		else:
			current = getattr(current, part)

	return current

def set_value(
	state: NarrativeState,
	path: str,
	operation: Operation,
	value: float | bool
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
    action: Action
) -> bool:

    for condition in action.preconditions:

        current_value = get_value(
            state,
            condition.path
        )

        comparator = operator.methodcaller(condition.operator, condition.value)

        if not comparator(current_value):
            return False

    return True


def apply_action(
	state: NarrativeState,
	action: Action
) -> NarrativeState:

	new_state = state.model_copy(deep=True)

	if not check_preconditions(new_state, action):
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
			success = check_preconditions(current_state, action)
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
	action_list: List[Action]
	success:bool
	selected_action: Action

	print("Welcome to GM-GENN-CRISS 0.3")
	print("\nThe story do you live next, start like this.")
	print(current_state)

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
				current_state = apply_action(current_state, selected_action)
				print("\n And the story continue like this")
				print(current_state)
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

	print("\nThank you for use GM-GENN_CRISS 0.3, have a nice day")

# -------------------------
# Estado inicial
# -------------------------

saul = Character(name="saul")

state = NarrativeState(
    characters={
        "saul": saul
    },
    tension=20
)


# -------------------------
# Acción
# -------------------------

kill_saul = Action(
	name="kill Saul",

	preconditions=[
		Condition(
			path="characters.saul.alive",
			operator=Comparison.EQUAL,
			value=True
		)
	],

	effects=[
		Effect(
			path="characters.saul.alive",
			operation= Operation.SET,
			value=False
		),

		Effect(
			path="tension",
			operation=Operation.INCREMENT,
			value=20
		)
	]
)

raise_tension = Action(
	name="raise tension",

	preconditions=[
		Condition(
			path="characters.saul.alive",
			operator=Comparison.EQUAL,
			value=False
		)
	],

	effects=[
		Effect(
			path="tension",
			operation=Operation.INCREMENT,
			value=10
		)
	]
)

cry_for = Action(
	name="cry for",

	preconditions=[
		Condition(
			path="tension",
			operator=Comparison.GREATER_EQUAL,
			value=50
		)
	],

	effects=[
		Effect(
			path="tension",
			operation=Operation.DECREMENT,
			value=10
		)
	]
)

graph = NarrativeGraph()

# -------------------------
# Transición
# -------------------------
initial_id = graph.add_state(state)

#new_states = expand_state(
#	graph,
#	state,
#	[
#		kill_saul,
#		raise_tension,
#		cry_for
#	]
#)

#state1 = graph.get_state(1)

#new_states = expand_state(
#    graph,
#    state1,
#    [
#        kill_saul,
#        raise_tension,
#        cry_for
#    ]
#)

#state2 = graph.get_state(2)

#print("\nNODOS")

#for node, data in graph.graph.nodes(data=True):
#	print(
#		"S" + str(node),
#		"-->",
#		data["state"]
#	)

#print("\nTRANSICIONES")

#for source, target, data in graph.graph.edges(data=True):
#	print(
#		"S" + str(source),
#		"--",
#		data["action"].name,
#		"-->",
#		"S" + str(target)
#   )

navigate(
	state,
	graph,
	[kill_saul, raise_tension, cry_for]
)