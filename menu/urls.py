from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryViewSet, MenuItemViewSet,
    DietaryTagViewSet, MenuVariationViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)
router.register(r'dietary-tags', DietaryTagViewSet)
router.register(r'variations', MenuVariationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]