from pydantic import BaseModel


# TODO: add more schemas
class FriendBase(BaseModel):
    symbol: str
    first_name: str
    last_name: str
