from pydantic import BaseModel, Field


class Home(BaseModel):
    version: str = Field(..., example="1.0.0")
    status: str = Field(..., example="OK")
