from typing import Annotated, Union
from fastapi import APIRouter, Cookie, Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[Union[str, None], Cookie()] = None,
):
    if not q:
        return last_query
    return q


@router.get("/", tags=["users"], summary="with dependency")
async def read_users(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)]
):
    """get users"""
    return {"q_or_cookie": query_or_default}


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}
