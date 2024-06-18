from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "$2a$12$7t3XVjWYxrd5yOU4C3N0POyD7k4PLmkPkygYgiiy8hyXFbXNR/24u"


router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool


class UserDB(User):
    password: str


users_db = {
    "gustavo": {
        "username": "gustavo",
        "full_name": "Gustavo Nievas",
        "email": "gustavonievas.com",
        "disable": False,
        "password": "$2a$12$nPuoEee1B9ssDrD0nGLDb.LZMSzZECadLhWM8h9/nHeH2OQVzO1/m"
    },
    "fernando": {
        "username": "fernando",
        "full_name": "Fernando Suarez",
        "email": "FernandoSuarez.com",
        "disable": True,
        "password": "$2a$12$nPuoEee1B9ssDrD0nGLDb.LZMSzZECadLhWM8h9/nHeH2OQVzO1/m"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    credentiiales_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid authentication credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    try:
        username: str = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise credentiiales_exception

    except jwt.JWTError as exc:
        raise credentiiales_exception from exc

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"})
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db: UserDB = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    access_token = {
        "sub": user.username,
        "exp":  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
            "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
