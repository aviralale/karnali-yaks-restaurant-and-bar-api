from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/menu/', include('menu.urls')),
    path('api/gallery/', include('gallery.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
