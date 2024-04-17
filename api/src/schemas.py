from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    name: str
    email: str


class CreateNoteSchema(BaseModel):
    user_id: int
    content: str
