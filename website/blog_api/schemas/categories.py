from ninja import Schema  # type: ignore
from datetime import datetime

class CategorySchema(Schema):
    id: int
    name: str
    slug: str
    created_at: datetime

class CategoryCreationSchema(Schema):
    name: str