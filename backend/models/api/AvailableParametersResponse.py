from pydantic import BaseModel


class AvailableParametersResponse(BaseModel):
    moves: list[str]
    algorithms: list[str]
