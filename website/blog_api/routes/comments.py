from typing import Union
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ninja import Router # type: ignore
from blog_api.schemas.comments import DeleteCommentSchema, CommentUpdateCreateSchema,CommentPaginatedSchema,CommentShortSchema
from blog_app.models import Comment
from blog_api.services.comment import comments_service

router = Router(
    tags=['Comments']
)

@router.get('/comments/', response=CommentPaginatedSchema)
def get_comments(request, limit: int = 5, offset: int = 0):
    return  comments_service.get_comments(limit=limit,offset=offset)

@router.get('/comments/{id}/', response=CommentShortSchema)
def get_comment_detail(request, id: int):
    return comments_service.get_comment_by_id(id=id)


@router.post('/comments/', response=CommentShortSchema)
def create_comment(request,comment_data: CommentUpdateCreateSchema):
    return comments_service.create_comment(comment_data=comment_data)

@router.put('/comments/{id}/update/',response=CommentShortSchema)
def update_comment(request, id:int, comment_data: CommentUpdateCreateSchema):
    return comments_service.update_comment(id=id, comment_data=comment_data)

@router.delete('/comments/{id}/', response=Union[DeleteCommentSchema,dict[str,str]])
def delete_comment(request,id:int):
    return comments_service.delete_comment(id=id)
