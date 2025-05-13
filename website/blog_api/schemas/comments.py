from datetime import datetime
from typing import Optional
from ninja import Schema# type: ignore
from .auth import UserSchema


class ArticleCommentSchema(Schema):
    id: int
    text: str
    author: UserSchema
    created_at: datetime

class CommentShortSchema(Schema):
    id: int
    text: str
    article_id: int
    author_id: int
    created_at: datetime

class CommentPaginatedSchema(Schema):
    total: int
    limit: int
    offset: int
    comments: list[CommentShortSchema]

class DeleteCommentSchema(Schema):
    is_deleted: bool

class CommentUpdateCreateSchema(Schema):
    article_id: int
    author_id: int
    text: str