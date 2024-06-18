from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.connect import db_client
from bson import ObjectId


router = APIRouter(prefix="/api/usersdb",
                   tags=["usersdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}})

users_list = []


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{user_id}", response_model=User)
async def user(user_id: str):
    found_user = search_user("_id", ObjectId(user_id))
    return found_user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: User):
    if isinstance(search_user("email", new_user.email), User):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    user_dict = dict(new_user)
    del user_dict["id"]

    id_new_user = db_client.users.insert_one(user_dict).inserted_id

    new_user_db = user_schema(
        db_client.users.find_one({"_id": id_new_user}))

    return User(**new_user_db)


@router.put("/{user_id}", response_model=User, status_code=status.HTTP_201_CREATED)
async def update_user(user_id: str, update_user: User):
    user_dict = dict(update_user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user_id)}, user_dict)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found") from exc

    return search_user("_id", ObjectId(user_id))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    found = db_client.users.find_one_and_delete(
        {"_id": ObjectId(user_id)})

    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def search_user(field: str, key):
    try:
        exist_user = db_client.users.find_one({field: key})
        return User(**user_schema(exist_user))
    except Exception:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
