from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}})

# Definiendo users con BaseModel de pydantic a JSON


class User(BaseModel):
    id: int  # Tipado con int
    name: str
    surname: str
    url: str
    age: int


users_list = [User(id=1, name="Gustavo", surname="Nievas", url="gustavonievas.com", age=22)]


@router.get("/usersjson")
async def usersjson():
    return [{"name": "Gustavo", "surname": "Nievas", "url": "gustavonievas.com", "age": 22},
            {"name": "Antonio", "surname": "Lopez",
                "url": "AntonioLopez.com", "age": 23},
            {"name": "Fernando", "surname": "Suarez", "url": "FernandoSuarez.com", "age": 24}]


@router.get("/", response_model=User)
async def users():
    return users_list

# Por Path


@router.get("/{user_id}", response_model=User)
async def user(user_id: int):
    return search_user(user_id)

# Por Query


@router.get("/user/", response_model=User)
async def userquery(user_id: int):
    return search_user(user_id)


@router.post("/", response_model=User, status_code=201)
async def create_user(new_user: User):
    if isinstance(search_user(new_user.id), User):
        raise HTTPException(status_code=400, detail="User already exists")
    users_list.append(new_user)
    return new_user


@router.put("/{user_id}", response_model=User, status_code=201)
async def update_user(user_id: int, new_user: User):
    if isinstance(search_user(user_id), User):
        new_user.id = user_id
        users_list.remove(search_user(user_id))
        users_list.append(new_user)
        return new_user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    if isinstance(search_user(user_id), User):
        users_list.remove(search_user(user_id))
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")


def search_user(user_id: int):
    all_users = filter(lambda user: user.id == user_id, users_list)
    try:
        return list(all_users)[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")
