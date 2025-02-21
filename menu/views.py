from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CategorySerializer, MenuItemSerializer,
    DietaryTagSerializer, MenuVariationSerializer
)
from .models import Category, MenuItem, DietaryTag, MenuVariation
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.OrderingFilter]

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        category = self.get_object()
        items = category.menuitem_set.all()
        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'dietary_tags', 'spice_level', 'is_special',]
    search_fields = ['name', 'description', 'name_spanish', 'description_spanish']

    @action(detail=False, methods=['get'])
    def specials(self, request):
        specials = self.queryset.filter(is_special=True)
        serializer = self.get_serializer(specials, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_dietary_preference(self, request):
        tag_id = request.query_params.get('tag')
        if tag_id:
            items = self.queryset.filter(dietary_tags__id=tag_id)
            serializer = self.get_serializer(items, many=True)
            return Response(serializer.data)
        return Response({'error': 'Tag parameter is required'}, status=400)

class DietaryTagViewSet(viewsets.ModelViewSet):
    queryset = DietaryTag.objects.all()
    serializer_class = DietaryTagSerializer

class MenuVariationViewSet(viewsets.ModelViewSet):
    queryset = MenuVariation.objects.all()
    serializer_class = MenuVariationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['menu_item']