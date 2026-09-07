import operator
import networkx as nx
from pydantic import BaseModel, Field
from src.narrative_engine.enum.operation import Operation
from src.narrative_engine.enum.comparison import Comparison
from src.narrative_engine.enum.mode import Mode
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

saul = Character(
    name="saul",
    pockets={
        "money": 50,
        "cigarettes": True
    }
)

amanda = Character(
    name="amanda",
    pockets={
        "money": 75,
        "vacuum bottle": True,
        "mate": True,
    }
)

bruce = Character(
    name="bruce",
    pockets={
        "money": 10,
        "guitar": True
    }
)

player = Character(
    name="player",
    pockets={
        "money": 20,
        "book": True
    }
)

state = NarrativeState(
    characters={
        "saul": saul,
        "amanda": amanda,
        "bruce": bruce,
        "player": player
    },
    happiness=60,
    calm=60,
    location="Junín"
)


# -------------------------
# Acción
# -------------------------

kill_saul = Action(
    name="kill Saul",
    mode= Mode.TERROR,

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
    mode= Mode.TERROR,

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
    mode= Mode.TERROR,

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
    mode= Mode.TERROR,

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
    mode= Mode.TERROR,

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

play_guitar = Action(
    name="play guitar",
    mode= Mode.RELAX,

    preconditions=Condition(
        path="characters.bruce.pockets.guitar",
        operator=Comparison.EQUAL,
        value=True
    ),

    effects=[
        Effect(
            path="happiness",
            operation=Operation.INCREMENT,
            value=10
        )
    ]
)

drink_mate = Action(
    name="drink mate",
    mode= Mode.RELAX,

    preconditions=ConditionAnd(
        conditions=[
            Condition(
                path="characters.amanda.pockets.mate",
                operator=Comparison.EQUAL,
                value=True
            ),
            Condition(
                path="characters.amanda.pockets.vacuum bottle",
                operator=Comparison.EQUAL,
                value=True
            )
        ]
    ),

    effects=[
        Effect(
            path="calm",
            operation=Operation.INCREMENT,
            value=5
        )
    ]
)

smoke_cigarette = Action(
    name="smoke cigarette",
    mode= Mode.RELAX,

    preconditions=Condition(
        path="characters.saul.pockets.cigarettes",
        operator=Comparison.EQUAL,
        value=True
    ),

    effects=[
        Effect(
            path="calm",
            operation=Operation.INCREMENT,
            value=5
        ),
        Effect(
            path="characters.saul.pockets.cigarettes",
            operation=Operation.SET,
            value=False
        )
    ]
)

buy_cigarette = Action(
    name="buy cigarette",
    mode= Mode.RELAX,

    preconditions=Condition(
        path="characters.saul.pockets.cigarettes",
        operator=Comparison.EQUAL,
        value=False
    ),

    effects=[
        Effect(
            path="characters.saul.pockets.cigarettes",
            operation=Operation.SET,
            value=True
        ),
        Effect(
            path="characters.saul.pockets.money",
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
    [kill_saul, kill_bruce, raise_tension, cry_for, run_away_amanda,
    play_guitar, drink_mate, smoke_cigarette, buy_cigarette]
)