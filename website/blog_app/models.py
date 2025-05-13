from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.

class Slider(models.Model):
    title = models.CharField(max_length=40, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='slider/',verbose_name='Фото')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Слайд'
        verbose_name_plural = 'Слайды'

class FAQ(models.Model):
    question = models.TextField(verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question
    
    class Meta:
        verbose_name='Вопрос ответ'
        verbose_name_plural='Вопросы ответы'

class Category(models.Model):
    name = models.CharField(max_length=40, unique=True, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг',help_text='Данное поле заполняется автоматическим')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(verbose_name='Слаг',unique=True)
    description = models.TextField(verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание', null=True,blank=True)
    preview = models.ImageField(upload_to='articles/previews', null=True,blank=True,verbose_name='Превью')
    views = models.PositiveIntegerField(default=0,verbose_name='Кол-во просмотров')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления',auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles',verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name='articles', verbose_name='Автор')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class ArticleImage(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE, verbose_name='Статья',related_name='images')
    photo = models.ImageField(upload_to='articles/gallery/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Галлерея статьи'
        verbose_name_plural = 'Галлерея статьи'

class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE, verbose_name='Статья',related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True,related_name='comments',verbose_name='Автор')
    text = models.TextField(verbose_name='Комментария')
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.article}'
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class ArticleCountView(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

class Like(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE,related_name='likes', verbose_name='Статья')
    user = models.ManyToManyField(User, related_name='likes')

class Dislike(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE,related_name='dislikes', verbose_name='Статья')
    user = models.ManyToManyField(User, related_name='dislikes')