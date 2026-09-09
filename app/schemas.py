from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TagOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title: str
    content: str
    tags: List[str] = []

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    author: UserOut
    tags: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        orm_mode = True

class ArticleList(BaseModel):
    items: List[ArticleOut]
    total: int
    page: int
    page_size: int