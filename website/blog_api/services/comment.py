from blog_api.schemas import comments
from blog_app.models import Comment,Article
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class CommentServise:
    def get_comments(self,limit: int=5, offset: int=0) -> comments.CommentPaginatedSchema:
        objects = Comment.objects.all()
        total_comments = objects.count()
        return comments.CommentPaginatedSchema(total=total_comments,
        offset=offset,
        limit=limit,
        comments=objects[offset:limit]                                    
        )
    
    def get_comment_by_id(self, id: int) -> Comment:
        comment = get_object_or_404(Comment, pk=id)
        return comment
    
    def create_comment(self, comment_data: comments.CommentUpdateCreateSchema) -> Comment:
        data = comment_data.dict()

        author = get_object_or_404(User, pk=data.pop('author_id'))
        article = get_object_or_404(Article, pk=data.pop('article_id'))
        new_comment = Comment.objects.create(text=data.get('text'), author=author, article=article)

        return new_comment
    
    def update_comment(self, id: int,comment_data: comments.CommentUpdateCreateSchema) -> Comment:
        comment = get_object_or_404(Comment, id=id)
        for key, value in comment_data.dict().items():
            setattr(comment, key, value)
        comment.save()
        return comment
    
    def delete_comment(self, id: int) -> dict:
        comment = get_object_or_404(Comment,pk=id)
        comment.delete()
        return{'is_deleted': True}

comments_service = CommentServise()