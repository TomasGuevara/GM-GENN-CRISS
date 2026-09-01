from __future__ import annotations
from pydantic import BaseModel, Field
from src.narrative_engine.enum.comparison import Comparison

class Condition(BaseModel):
	path: str
	operator: Comparison
	value: float | bool

class ConditionOr(BaseModel):
	conditions: list[Condition|ConditionAnd]

class ConditionAnd(BaseModel):
	conditions: list[Condition|ConditionOr]