from django.urls import path
from apps.articles import views


urlpatterns = [
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('commercial/', views.AdView.as_view(), name='commercial'),
    path('medias/', views.MediasView.as_view(), name='medias'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/most-viewed/', views.ArticleMostViewed.as_view(), name='most_viewed_articles'),
    path('articles/search/', views.ArticleSearchView.as_view(), name='search_articles'),
    path('articles/interesting/', views.ArticleInterestingView.as_view(), name='article_interesting'),
    path('articles/<field>/<media>/', views.ArticleFilterByPhotoOrVideo.as_view(), name='filter_by_photo_or_video'),
]
