from pydantic import BaseModel


class UserIdentity(BaseModel):
    email: str
    id: str
