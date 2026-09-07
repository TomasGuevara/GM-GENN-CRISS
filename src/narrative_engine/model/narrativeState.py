from pydantic import BaseModel, Field
from src.narrative_engine.model.character import Character

class NarrativeState(BaseModel):
	characters: dict[str, Character]
	tension: float = 0
	happiness: float = 0
	calm: float = 0
	location: str
	flags: dict[str, bool | str | float] = Field(default_factory=dict)