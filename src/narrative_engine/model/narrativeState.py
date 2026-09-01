from pydantic import BaseModel, Field
from src.narrative_engine.model.character import Character

class NarrativeState(BaseModel):
	characters: dict[str, Character]
	tension: float
	location: str
	flags: dict[str, bool | str | float] = Field(default_factory=dict)