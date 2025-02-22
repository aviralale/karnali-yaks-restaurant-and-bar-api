from django.contrib import admin
from .models import Photo, Video, Tag
from django.core.exceptions import ValidationError

# Inline classes (optional)
class TagInline(admin.TabularInline):
    model = Photo.tags.through  # For managing tags inline with Photos
    extra = 1

# Admin classes
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Automatically generate slug from name
    search_fields = ('name',)

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_featured', 'views_count', 'location', 'camera_model')
    list_filter = ('is_featured', 'tags', 'uploaded_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('uploaded_at', 'views_count', )  # Prevent editing these fields
    inlines = [TagInline]  # Optional: Add tags inline
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'caption', 'location', 'camera_model', 'taken_at')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'views_count',  'is_featured', 'order')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )

    def save_related(self, request, form, formsets, change):
        # Ensure no duplicate tags are added
        tags = form.cleaned_data.get('tags', [])
        if len(tags) != len(set(tags)):
            raise ValidationError("Duplicate tags are not allowed.")
        super().save_related(request, form, formsets, change)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'is_featured', 'views_count' , 'duration', 'is_processed')
    list_filter = ('is_featured', 'is_processed', 'tags', 'uploaded_at')
    search_fields = ('title', 'description')
    readonly_fields = ('uploaded_at', 'views_count', )  # Prevent editing these fields
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'video', 'thumbnail', 'duration', 'is_processed')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'views_count', 'is_featured', 'order')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )