from dataclasses import dataclass
from typing import Protocol

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# core domain model
@dataclass
class User:
    id: str
    name: str


# port (interface)
class UserRepository(Protocol):
    def add_user(self, user: User) -> User:
        ...
    
    def get_user(self, user_id: str) -> User | None:
        ...

# core application service
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_id: str, name: str):
        user = User(user_id, name)
        return self.repository.add_user(user)

    def find_user(self, user_id: str):
        return self.repository.get_user(user_id)

# adapter for repository
class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self.users: dict[str, User] = {}

    def add_user(self, user: User) -> User:
        self.users[user.id] = user
        print(user)
        return user

    def get_user(self, user_id: str) -> User | None:
        return self.users.get(user_id)

# dependency for FastAPI
def get_repository() -> UserRepository:
    return InMemoryUserRepository()

# adapter for fastAPI
app = FastAPI()

class UserCreate(BaseModel):
    id: str
    name: str

@app.post("/user")
def create_user(user: UserCreate, repo: UserRepository = Depends(get_repository)):
    service = UserService(repo)
    created_user = service.create_user(user.id, user.name)
    return created_user

@app.get("/user/{user_id}")
def read_user(user_id: str, repo: UserRepository = Depends(get_repository)):
    service = UserService(repo)
    user = service.find_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
