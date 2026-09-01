import operator
import networkx as nx
from pydantic import BaseModel, Field
from src.narrative_engine.enum.operation import Operation
from src.narrative_engine.enum.comparison import Comparison
from src.narrative_engine.model.character import Character
from src.narrative_engine.model.narrativeState import NarrativeState
from src.narrative_engine.model.condition import Condition, ConditionAnd, ConditionOr
from src.narrative_engine.model.effect import Effect
from src.narrative_engine.model.action import Action
from src.narrative_engine.graph.narrativeGraph import NarrativeGraph
from src.narrative_engine.narrative_state.representNarrativeState import navigate

# -------------------------
# Estado inicial
# -------------------------

saul = Character(name="saul")

amanda = Character(name="amanda")

bruce = Character(name="bruce")

state = NarrativeState(
    characters={
        "saul": saul,
        "amanda": amanda,
        "bruce": bruce
    },
    tension=20,
    location="Junín"
)


# -------------------------
# Acción
# -------------------------

kill_saul = Action(
    name="kill Saul",

    preconditions=Condition(
        path="characters.saul.alive",
        operator=Comparison.EQUAL,
        value=True
    ),

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

kill_bruce = Action(
    name="kill Bruce",

    preconditions=Condition(
        path="characters.bruce.alive",
        operator=Comparison.EQUAL,
        value=True
    ),

    effects=[
        Effect(
            path="characters.bruce.alive",
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

    preconditions=ConditionOr(
        conditions=[
            Condition(
                path="characters.saul.alive",
                operator=Comparison.EQUAL,
                value=False
            ),

            Condition(
                path="characters.bruce.alive",
                operator=Comparison.EQUAL,
                value=False
            )
        ]
    ),

    effects=[
        Effect(
            path="tension",
            operation=Operation.INCREMENT,
            value=10
        )
    ]
)

run_away_amanda = Action(
    name="run away with Amanda",

    preconditions=ConditionAnd(
        conditions=[
            Condition(
                path="characters.saul.alive",
                operator=Comparison.EQUAL,
                value=False
            ),

            Condition(
                path="characters.bruce.alive",
                operator=Comparison.EQUAL,
                value=False
            ),

            Condition(
                path="characters.amanda.flags.escaped",
                operator=Comparison.EQUAL,
                value=False
            )
        ]
    ),

    effects=[
        Effect(
            path="tension",
            operation=Operation.DECREMENT,
            value=30
        ),

        Effect(
            path="characters.amanda.flags.escaped",
            operation=Operation.SET,
            value=True
        ),

        Effect(
            path="flags.place",
            operation=Operation.SET,
            value="Plaza Sarmiento"
        ),
    ]
)

cry_for = Action(
    name="cry for",

    preconditions=Condition(
        path="tension",
        operator=Comparison.GREATER_EQUAL,
        value=50
    ),

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

navigate(
    state,
    graph,
    [kill_saul, kill_bruce, raise_tension, cry_for, run_away_amanda]
)