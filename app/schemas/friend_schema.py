from pydantic import BaseModel

class FriendBase(BaseModel):
    symbol: str
    first_name: str
    last_name: str

# class FriendCreate(FriendBase):
#     pass

class FriendUpdate(FriendBase):
    pass

# class FriendResponse(FriendBase):
#     class Config:
#         orm_mode = True