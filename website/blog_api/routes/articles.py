import os
from ninja import Router, File, Form # type: ignore
from blog_api.schemas.articles import ArticlelistSchema,ArticlesPaginatedSchema,ArticledetailSchema,ArticleCreateSchema,ArticleDeleteSchema,ArticleUpdateSchema
from blog_app.models import Article, Category, ArticleImage
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from typing import Optional, Union
from ninja.files import UploadedFile # type: ignore
from ninja.security import django_auth # type: ignore
from website.settings import BASE_DIR
import os
from blog_api.services.article import article_service

router = Router(
    tags=['Articles']
)

@router.get('/articles/',response=ArticlesPaginatedSchema)
def get_articles(request, offset: int = 0, limit: int = 2):
    return article_service.get_paginated_articles(limit, offset)

@router.get('/articles/{slug}',response=ArticledetailSchema)
def get_article_detail(request,slug: str):
    return article_service.get_article_detail(slug)


@router.post('/articles/', response=ArticledetailSchema)
def create_new_article(request, data: Form[ArticleCreateSchema],
preview: Optional[UploadedFile] = File(None), gallery: Optional[list[UploadedFile]] = File(None)):
    return article_service.create_new_article(data=data, preview=preview, gallery=gallery)


@router.patch('/articles/{id}/update/', response=ArticledetailSchema)
def update_article(request, id: int, data: ArticleUpdateSchema,
preview: Optional[UploadedFile] = File(None), gallery: Optional[list[UploadedFile]] = File(None)):
    return article_service.update_article(id=id, data=data, preview=preview, gallery=gallery)

@router.delete('/articles/{id}/',response=Union[ArticleDeleteSchema,dict[str,str]])
def delete_article(request, id: int):
    return article_service.delete_article(id=id)