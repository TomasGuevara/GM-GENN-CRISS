from pydantic import BaseModel, Field

class NarrativeHistory(BaseModel):
    scenes: list[str] = []