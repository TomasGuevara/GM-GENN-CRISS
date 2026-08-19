import operator
from pydantic import BaseModel
from operation import Operation
from comparison import Comparison

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
	target: str
	preconditions: list[Condition]
	effects: list[Effect]

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

	character = new_state.characters[action.target]

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

def navigate(
	state: NarrativeState,
	actions: list[Action]
):
	current_state = state
	user_input = ""
	action_list: List[Action]
	success:bool
	selected_action: Action

	print("Welcome to GM-GENN-CRISS 0.2")
	print("\nThe story do you live next, start like this.")
	print(current_state)

	while user_input != "Close system":
		action_list = get_available_action(current_state, actions)
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
				print("\n You can do the next actions")

			else:
				print("\nThe action selected doesn't exist in the actions list mentioned.")
				print("\nWould you write one of the next options?")

	print("\nThank you for use GM-GENN_CRISS 0.1, have a nice day")

# -------------------------
# Estado inicial
# -------------------------

ana = Character(name="Ana")

state = NarrativeState(
    characters={
        "ana": ana
    },
    tension=20
)


# -------------------------
# Acción
# -------------------------

kill_ana = Action(
	name="kill Ana",

	target="ana",

	preconditions=[
		Condition(
			path="characters.ana.alive",
			operator=Comparison.EQUAL,
			value=True
		)
	],

	effects=[
		Effect(
			path="characters.ana.alive",
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

	target="ana",

	preconditions=[
		Condition(
			path="characters.ana.alive",
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

	target="ana",

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

# -------------------------
# Transición
# -------------------------

navigate(
	state,
	[kill_ana, raise_tension, cry_for]
)