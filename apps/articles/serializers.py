from rest_framework import serializers
from apps.articles.models import (
    Article, Category, Media, Contact, Image, Video, Ad,
)


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['image', 'link']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video', 'file', 'thumbnail']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image',]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'title', 'created', 'updated', 
        ]


class MediaObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Image):
            serializer = ImageSerializer(value, context=self.context)
        elif isinstance(value, Video):
            serializer = VideoSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data


class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category', read_only=True)
    media = MediaObjectRelatedField(read_only=True)
    region = serializers.SerializerMethodField()
    images = ImageSerializer(read_only=True, many=True)

    def get_region(self,obj):
        return obj.get_region_display()
    
    class Meta:
        model = Article
        fields = [
            'id', 'category', 'region', 'category_name', 'title', 'body', 'is_interesting', 
            'created', 'updated', 'media', 'viewed', 'images'
        ]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = [
            'instagram', 'telegram', 'youtube', 'facebook', 
        ]


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
           'address', 'email', 'phone'
        ]
