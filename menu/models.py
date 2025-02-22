from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    es_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class DietaryTag(models.Model):
    name = models.CharField(max_length=50)
    es_name = models.CharField(max_length=50, blank=True)
    icon = models.CharField(max_length=255)  # For storing icon class/identifier
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    SPICE_LEVELS = [
        (1, 'Mild'),
        (2, 'Medium'),
        (3, 'Hot'),
    ]
    name = models.CharField(max_length=200)
    name_spanish = models.CharField(max_length=200, blank=True)  # For Spanish translations
    description = models.TextField(blank=True)
    description_spanish = models.TextField(blank=True)
    price = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dietary_tags = models.ManyToManyField(DietaryTag, blank=True)
    spice_level = models.IntegerField(choices=SPICE_LEVELS, null=True, blank=True)
    is_special = models.BooleanField(default=False)
    order = models.IntegerField(default=0)


    class Meta:
        ordering = ['category','order']

    def __str__(self):
        return f"{self.order}. {self.name}"

class MenuVariation(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='variations')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.menu_item.name} - {self.name}"