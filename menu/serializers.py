from rest_framework import serializers
from .models import Category, MenuItem, DietaryTag, MenuVariation

class DietaryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryTag
        fields = ['id', 'name', 'icon', 'description']

class MenuVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuVariation
        fields = ['id', 'name', 'price']

class MenuItemSerializer(serializers.ModelSerializer):
    dietary_tags = DietaryTagSerializer(many=True, read_only=True)
    variations = MenuVariationSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'name_spanish', 
            'description', 'description_spanish', 
            'price', 'category', 'category_name',
            'dietary_tags', 'variations', 'spice_level',
            'is_special'
        ]

class CategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(source='menuitem_set', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description',  'items']