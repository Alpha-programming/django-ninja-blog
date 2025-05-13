import os
from typing import Optional
from django.shortcuts import get_object_or_404
from blog_api.schemas.articles import ArticleCreateSchema, ArticlesPaginatedSchema,ArticleUpdateSchema
from blog_app.models import Article, ArticleImage, Category
from ninja.files import UploadedFile # type: ignore
from django.contrib.auth.models import User
from website.settings import BASE_DIR


class ArticleService:
    def __save_photo(self, file: UploadedFile, folder_path: str):
        file = file.read()
        with open(folder_path, mode='wb') as _file:
            _file.write(file)

    def create_new_article(self, data: ArticleCreateSchema, preview: Optional[UploadedFile],gallery: Optional[list[UploadedFile]]):
        _data = data.dict()

        category = get_object_or_404(Category, pk=_data.pop('category'))
        author = get_object_or_404(User, pk=_data.pop('author'))
        article = Article.objects.create(**_data, category=category, author=author)

        if preview is not None:
            preview_path = f'{BASE_DIR}/media/articles/previews/{preview.name}'
            self.__save_photo(preview, preview_path)
            article.preview = f'articles/previews/{preview.name}'
            article.save()

        for item in gallery:
            item_path = f'{BASE_DIR}/media/articles/gallery/{item.name}'
            self.__save_photo(item, item_path)

            obj = ArticleImage.objects.create(
                article=article,
                photo = f'articles/gallery/{item.name}'
            )
        return article

    def get_paginated_articles(
            self, limit: int = 2, offset: int=0) -> ArticlesPaginatedSchema:
        articles = Article.objects.all()
        total = articles.count()

        articles = articles[offset:limit]

        return ArticlesPaginatedSchema(
            total=total,
            offset=offset,
            limit=limit,
            articles=articles
        )
    
    def get_article_detail(self, slug: str) -> Article:
        articles = get_object_or_404(Article, slug=slug)
        return articles
    
    def delete_article(self, id: int) -> dict:
        article = get_object_or_404(Article,pk=id)
        article.delete()
        return{'is_deleted': True}
    
    def update_article(self, id: int, data: ArticleUpdateSchema, preview: Optional[UploadedFile],gallery: Optional[list[UploadedFile]]) -> Article:
        article = get_object_or_404(Article,pk=id)
        for key, value in data.dict().items():
            if not value:
                current_value = getattr(article, key)
                setattr(article, key, current_value)
            else:
                if key == 'category':
                    category = get_object_or_404(Category, pk=value)
                    setattr(article, key, category)
                else:
                    setattr(article, key, value)
        article.save()

        if preview is not None:
            preview_content = preview.read()
            if article.preview:
                os.remove(f'{BASE_DIR}/{article.preview.url}')

            with open(f'{BASE_DIR}/media/articles/previews/{preview.name}', mode='wb') as file:
                file.write(preview_content)
        
            article.preview = f'articles/previews/{preview.name}'
            article.save()
            
        if gallery is not None:
            for item in article.images.all():
                os.remove(f'{BASE_DIR}/{item.photo.url}')
                item.delete()
            
            for item in gallery:
                item_bytes = item.read()
                with open(f'{BASE_DIR}/media/articles/gallery/{item.name}', mode='wb') as file:
                    file.write(item_bytes)
                obj = ArticleImage.objects.create(
                    article=article,
                    photo = f'articles/gallery/{item.name}'
                )
        return article
                
        
    
article_service = ArticleService()