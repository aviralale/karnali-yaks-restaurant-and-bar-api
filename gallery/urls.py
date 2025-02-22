from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PhotoViewSet, VideoViewSet, TagViewSet

router = DefaultRouter()
router.register(r'photos', PhotoViewSet)
router.register(r'videos', VideoViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
