from datetime import datetime
from ninja import Schema# type: ignore
from blog_app.models import Article
from .comments import ArticleCommentSchema
from .categories import CategorySchema
from typing import Optional
from .auth import UserSchema




class ArticlelistSchema(Schema):
    id: int
    title: str
    slug: str
    description: str
    preview: Optional[str]
    views: int
    category: CategorySchema
    author: UserSchema
    created_at: datetime
    
class ArticlesPaginatedSchema(Schema):
    total: int
    offset: int=0
    limit: int=2 
    articles: list[ArticlelistSchema]   


class ArticleImageSchema(Schema):
    id: int
    photo: str

class ArticledetailSchema(Schema):
    id: int
    title: str
    slug: str
    description: str
    full_description: Optional[str]
    preview: Optional[str]
    views: int
    category: CategorySchema
    author: UserSchema
    comments: Optional[list[ArticleCommentSchema]]
    total_likes: int = 0
    total_dislikes: int = 0
    total_comments: int = 0
    created_at: datetime
    updated_at: datetime
    images: Optional[list[ArticleImageSchema]]

    @staticmethod
    def resolve_total_likes(obj: Article):
        return obj.likes.user.all().count()
    
    @staticmethod
    def resolve_total_dislikes(obj: Article):
        return obj.dislikes.user.all().count()
    
    @staticmethod
    def resolve_total_comments(obj: Article):
        return obj.comments.all().count()
    
    
class ArticleCreateSchema(Schema):
    title: str
    description: str
    full_description: Optional[str] = None
    category: int
    author: int


class ArticleDeleteSchema(Schema):
    is_deleted: bool

class ArticleUpdateSchema(Schema):
    title: Optional[str] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    category: Optional[int] = None
    