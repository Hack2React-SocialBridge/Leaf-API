from pydantic import BaseModel


class DetailsResponseSchema(BaseModel):
    detail: str
