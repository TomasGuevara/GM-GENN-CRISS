from pydantic import BaseModel, Field

class Character(BaseModel):
	name: str
	alive: bool = True
	flags: dict[str, bool | str | float] = Field(default_factory=dict)