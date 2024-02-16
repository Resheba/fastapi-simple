from pydantic import BaseModel, Field, SecretStr


class UserInSchema(BaseModel):
    name: str = Field(max_length=30)
    password: SecretStr


class UserOutSchema(BaseModel):
    name: str
