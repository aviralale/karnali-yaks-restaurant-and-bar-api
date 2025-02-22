from rest_framework import serializers
from .models import Photo, Video, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class PhotoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tag.objects.all(), source='tags'
    )

    class Meta:
        model = Photo
        fields = [
            'id', 'title', 'description', 'image', 'tags', 'tag_ids',
            'uploaded_at', 'is_featured', 'views_count',
            'caption', 'location', 'camera_model', 'taken_at', 'order'
        ]

class VideoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Tag.objects.all(), source='tags'
    )

    class Meta:
        model = Video
        fields = [
            'id', 'title', 'description', 'video', 'thumbnail', 'tags', 'tag_ids',
            'uploaded_at', 'is_featured', 'views_count',
            'duration', 'is_processed', 'order'
        ]
