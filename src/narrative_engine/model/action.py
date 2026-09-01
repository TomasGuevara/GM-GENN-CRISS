from pydantic import BaseModel, Field
from src.narrative_engine.model.effect import Effect
from src.narrative_engine.model.condition import Condition, ConditionAnd, ConditionOr

class Action(BaseModel):
	name: str
	preconditions: Condition|ConditionAnd|ConditionOr
	effects: list[Effect]