from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from apps.articles.models import (
    Article, Category, Contact, Media, Image, Video, Ad
)
from django.contrib.contenttypes.admin import (
    GenericTabularInline, GenericStackedInline
)
from django import forms


class ImageOrVideoFilter(SimpleListFilter):
    title = "Изображение/Видео"  # a label for our filter
    parameter_name = "media"  # you can put anything here

    def lookups(self, request, model_admin):
        # This is where you create filter options; we have two:
        return [
            ("video", "Видео"),
            ("image", "Изображение"),
        ]

    def queryset(self, request, queryset):
        # This is where you process parameters selected by use via filter options:
        if self.value() == "image":
            # Get websites that have at least one page.
            return queryset.distinct().filter(images__isnull=False)
        if self.value():
            # Get websites that don't have any pages.
            return queryset.distinct().filter(images__isnull=True)


class MainArticleForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'category', 'title', 'body',
            'is_interesting', 'viewed', 'region'
        ]


# class ImageProxy(Image):
#     class Meta:
#         proxy = True
#         verbose_name = 'Главная новость'
#         verbose_name_plural = 'Главная новость'


class ArticleMainProxy(Article):
    class Meta:
        proxy = True
        verbose_name = 'Главная новость'
        verbose_name_plural = 'Главная новость'


class ArticleImageForm(ArticleForm):
    class Meta:
        fields = [
            'category', 'title', 'body',
            'is_interesting',  'viewed', 'region'
        ]


class ArticleImageProxyForm(ArticleForm):

    def clean(self):
        if not self.instance.pk and Article.objects.filter(is_main=True).count() >= 1:
            # if you'll not check for self.pk 
            # then error will also raised in update of exists model
            raise forms.ValidationError('There is can be only one Main Article!')
        self.instance.is_main = 1
        return self.cleaned_data


class ArticleInline(GenericStackedInline):
    form = ArticleImageForm
    model = Article
    extra = 1


class ArticleInlineProxy(GenericStackedInline):
    form = ArticleImageProxyForm
    model = Article
    extra = 1


class ArticleInlineForCategory(admin.StackedInline):
    model = Article
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'created', 'updated',
    ]
    search_fields = ['title',]
    list_filter = [
        'created', 'updated', 'articles'
    ]
    inlines = [ArticleInlineForCategory]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    inlines = [ArticleInline]
    list_display = ['video', 'file',]
    empty_value_display = 'Нету видео'


# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     list_display = ['image']
#     inlines = [ArticleInline,]


class ImageInline(admin.StackedInline):
    model = Image


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleImageForm
    list_display = [ 
        'category', 'title', 'body',
        'created', 'updated'
    ]
    search_fields = ['title', 'body']
    list_filter = [ImageOrVideoFilter, 'is_main', 'is_interesting', 'created', 'updated']
    inlines = [ImageInline,]


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = [ 
        'note', 'image',
    ]
    list_filter = ['created', 'updated',]


# main article
# @admin.register(ImageProxy)
# class ImageProxyAdmin(admin.ModelAdmin):
#     # list_display = ['image']
#     #  actions = None
#     form = MainArticleForm
#     inlines = [ArticleInlineProxy,]

#     def get_queryset(self, request):
#         # qs = super(ImageProxyAdmin, self).get_queryset(request)
#         qs = Article.objects.all()
#         return qs.filter(is_main=1)



@admin.register(ArticleMainProxy)
class ArticleMainProxyAdmin(admin.ModelAdmin):
    form = ArticleImageProxyForm
    list_display = [ 
        'category', 'title', 'body',
        'created', 'updated'
    ]
    list_filter = ['is_main', 'is_interesting', 'created', 'updated',]
    inlines = [ImageInline,]

    def get_queryset(self, request):
        # qs = super(ImageProxyAdmin, self).get_queryset(request)
        qs = Article.objects.all()
        return qs.filter(is_main=1)

admin.site.register(Contact)
admin.site.register(Media)
