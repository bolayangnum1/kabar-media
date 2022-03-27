from django.db import models
from apps.articles.choices import REGION_CHOICES
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
# from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from apps.articles.validators import validate_file_extension


class Video(models.Model):
    video = models.URLField(
        verbose_name='Видео', blank=True, null=True
    )
    file = models.FileField(
        upload_to='videos/', verbose_name='Загружаемое видео', blank=True, null=True,
        validators=[validate_file_extension]
    )
    thumbnail = models.ImageField(
        upload_to='thumbnails/', verbose_name='Превью для видео', blank=True, null=True
    )
    articles = GenericRelation('Article')

    def __str__(self):
        return f'video with id: {self.id}'

    class Meta:
        verbose_name = 'Новость с Видео'
        verbose_name_plural = 'Новости с Видео'
        ordering = ('-id',)


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().filter(is_interesting=False)

class Article(models.Model):
    category = models.ForeignKey(
        'Category', related_name='articles', on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=255, verbose_name='Заголовок',
    )
    body = models.TextField(
        verbose_name='Тело поста'
    )
    is_main = models.BooleanField(
        verbose_name='Главный пост', default=False
    )
    is_interesting = models.BooleanField(
        default=False, verbose_name='Интересное?'
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('video',)},
        verbose_name='Изображение/Видео', null=True, blank=True
    )
    object_id = models.PositiveIntegerField(
        'Id объекта медиа', null=True, blank=True
    )
    media = GenericForeignKey(
        'content_type', 'object_id',
    )
    viewed = models.PositiveIntegerField(
        default=0, verbose_name='Просмотрено', blank=True
    )
    region = models.PositiveSmallIntegerField(
        verbose_name='Область/Регион', choices=REGION_CHOICES
    )
    created = models.DateTimeField(
        'Создан', auto_now_add=True, 
    )
    updated = models.DateTimeField(
        'Обновлен', auto_now=True
    )
    # objects = ArticleManager()
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-created',)


class Image(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='images', 
        verbose_name='Новость', null=True, blank=True
    )
    image = models.ImageField(
        upload_to='articles/', verbose_name='Изображение',
    )

    def __str__(self):
        return f'image with id: {self.id}'

    class Meta:
        verbose_name = 'Новость с Изображением'
        verbose_name_plural = 'Новости с Изображением'
        ordering = ('-id',)


class Category(models.Model):
    title = models.CharField(
        max_length=255, verbose_name='Заголовок'
    )
    created = models.DateTimeField(
        'Создан',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        'Обновлен',
        auto_now=True
    )
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-created',)


class Contact(models.Model):
    address = models.CharField(
        max_length=255, verbose_name='Адрес'
    )
    email = models.EmailField(
        unique=True, blank=True, null=True, verbose_name='Почта'
    )
    phone = models.CharField(
        max_length=30, verbose_name='Телефон'
    )

    def __str__(self):
        return f'Контакт с номером: {self.phone}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Media(models.Model):
    instagram = models.URLField(
        max_length=255, verbose_name='Инстаграм'
    )
    telegram = models.URLField(
        max_length=255, verbose_name='Телеграм'
    )
    youtube = models.URLField(
        max_length=255, verbose_name='Ютуб'
    )
    facebook = models.URLField(
        max_length=255, verbose_name='Фейсбук'
    )
    
    def __str__(self):
        return f'Ссылки в соц-сети {self.id}'

    class Meta:
        verbose_name = 'Медиа ссылка'
        verbose_name_plural = 'Медиа ссылки'


class Ad(models.Model):
    note = models.CharField(
        max_length=255, verbose_name='Заметка', blank=True
    )
    link = models.URLField(
        verbose_name='Ссылка на заказчика'
    )
    image = models.ImageField(
        upload_to='advertising/', verbose_name='Изображение'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан'
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name='Обновлен'
    )

    def __str__(self):
        return f'Реклама с номером: {self.id}, Заметка к рекламе{self.note}'
    
    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламы'
