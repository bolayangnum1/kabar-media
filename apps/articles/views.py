from rest_framework import generics, mixins
from rest_framework import filters as drf_filters
from django_filters import rest_framework as filters
from rest_framework.response import Response
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import APIException
from apps.articles.serializers import (
    AdSerializer, ArticleSerializer, CategorySerializer, ContactSerializer, MediaSerializer,
    
)
from apps.articles.models import (
    Article, Category, Media, Contact, Ad, 
)
# from rest_framework.pagination import LimitOffsetPagination
from apps.articles.pagination import StandardResultsSetPagination


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category', 'region', 'is_main')


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.viewed += 1
        obj.save(update_fields=("viewed", ))
        return super().retrieve(request, *args, **kwargs)


class ArticleMostViewed(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category', 'region')
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().order_by('-viewed'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ArticleSearchView(generics.ListAPIView):
    search_fields = ['title', 'body']
    filter_backends = (drf_filters.SearchFilter,)
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class ArticleFilterByPhotoOrVideo(generics.ListAPIView):
    queryset = Article.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = ArticleSerializer
    filterset_fields = ('region',)
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        media = kwargs.get('media')
        field = kwargs.get('field')
        if media == 'video':
            try:
                ctype = ContentType.objects.get(app_label='articles', model=media)
                queryset = self.filter_queryset(self.get_queryset()).filter(content_type=ctype)
                queryset = queryset.filter(images=None)
                if field == 'viewed':
                    queryset = queryset.order_by('-viewed')
                elif field == 'is_interesting':
                    queryset = queryset.filter(is_interesting=True).order_by('-viewed')
                else:
                    raise APIException("Need to pass valid field param!")
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                serializer = self.get_serializer(queryset, many=True)
                return Response(serializer.data)
            except:
                raise APIException("Need to pass valid field param!")
        elif media == 'image':
            queryset = self.filter_queryset(self.get_queryset().filter(object_id__isnull=True))
            if field == 'viewed':
                queryset = queryset.order_by('-viewed')
            elif field == 'is_interesting':
                queryset = queryset.filter(is_interesting=True).order_by('-viewed')
            else:
                raise APIException("Need to pass valid field param!")
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            raise APIException("Need to pass valid field param!")


class ArticleInterestingView(generics.ListAPIView):
    queryset = Article.objects.filter(is_interesting=True)
    serializer_class = ArticleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category', 'region')
    pagination_class = StandardResultsSetPagination


class CategoriesView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MediasView(generics.ListAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class ContactsView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ContactsView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class AdView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
