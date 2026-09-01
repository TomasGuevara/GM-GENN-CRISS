from pydantic import BaseModel, Field
from src.narrative_engine.enum.operation import Operation

class Effect(BaseModel):
	path: str
	operation: Operation
	value: float | bool | str