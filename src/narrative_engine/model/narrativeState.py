from pydantic import BaseModel, Field
from src.narrative_engine.model.character import Character

class NarrativeState(BaseModel):
	characters: dict[str, Character]
	moods: dict[str, bool | str | float] = Field(default_factory=dict)
	location: str
	flags: dict[str, bool | str | float] = Field(default_factory=dict)