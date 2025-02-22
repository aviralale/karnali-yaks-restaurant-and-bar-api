from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class BaseMedia(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ['order', '-uploaded_at']

class Photo(BaseMedia):
    image = models.ImageField(
        upload_to='gallery/photos/%Y/%m',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])]
    )
    caption = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    camera_model = models.CharField(max_length=100, blank=True)
    taken_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class Video(BaseMedia):
    video = models.FileField(
        upload_to='gallery/videos/%Y/%m',
        validators=[FileExtensionValidator(['mp4', 'mov', 'avi'])]
    )
    thumbnail = models.ImageField(upload_to='gallery/videos/thumbnails/%Y/%m', blank=True)
    duration = models.DurationField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
