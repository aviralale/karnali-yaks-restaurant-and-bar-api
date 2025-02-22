from django.contrib import admin
from .models import Category, MenuItem, DietaryTag, MenuVariation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)

class MenuVariationInline(admin.TabularInline):
    model = MenuVariation
    extra = 1

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'category', 'price', )
    list_filter = ('category', 'dietary_tags', 'order')
    search_fields = ('name', 'description')
    inlines = [MenuVariationInline]
    filter_horizontal = ('dietary_tags',)

@admin.register(DietaryTag)
class DietaryTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')