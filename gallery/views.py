from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Photo, Video, Tag
from .serializers import PhotoSerializer, VideoSerializer, TagSerializer

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags', 'is_featured']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['uploaded_at', 'order']
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        photo = self.get_object()
        photo.views_count += 1
        photo.save()
        return Response({'status': 'viewed'})

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags', 'is_featured', 'is_processed']
    search_fields = ['title', 'description']
    ordering_fields = ['uploaded_at', 'order']
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def view(self, request, pk=None):
        video = self.get_object()
        video.views_count += 1
        video.save()
        return Response({'status': 'viewed'})

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
