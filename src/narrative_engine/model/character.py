from pydantic import BaseModel, Field

class Character(BaseModel):
	name: str
	attributes: dict[str, bool | str | float] = Field(default_factory=dict)
	pockets: dict[str, bool | str | float] = Field(default_factory=dict)
	effect: dict[str, bool | str | float] = Field(default_factory=dict)