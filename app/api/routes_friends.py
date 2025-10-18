"""Friends related API routes."""
from fastapi import APIRouter, HTTPException

from app.models.friend import Friend
from app.services.friend_service import FriendService

router = APIRouter()
friend_service = FriendService()

# TODO:
#  - have a response model via schemas
#  - allow for JSON formatted input/output
#

@router.get("/friends", response_model=None)
def list_friends() -> list[Friend]:
    """List all Friends."""
    friends = friend_service.friend_repo.get_all()
    return friends


@router.get("/friends/{symbol}", response_model=None)
def get_friend(symbol: str) -> Friend:
    """Retrieve a Friend by symbol."""
    friend = friend_service.get_friend(symbol)
    if friend is None:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend


@router.post("/friends/", response_model=None)
def create_friend(symbol: str, first_name: str, last_name: str) -> Friend:
    """Create a new Friend."""
    try:
        friend = friend_service.create_friend(symbol, first_name, last_name)
        return friend
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/friends/{symbol}", response_model=dict)
def delete_friend(symbol: str) -> dict:
    """Delete a Friend by symbol."""
    try:
        result = friend_service.remove_friend(symbol)
        if not result:
            raise HTTPException(status_code=404, detail="Friend not found")
        return {"result": "Friend deleted"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/friends/{symbol}/", response_model=None)
def update_friend(symbol: str, new_symbol: str = None,
                    first_name: str = None, last_name: str = None) -> Friend:
    """Update an existing Friend's details."""
    try:
        friend = friend_service.modify_friend(symbol, new_symbol, first_name, last_name)
        return friend
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
