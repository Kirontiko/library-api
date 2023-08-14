from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("book.urls", namespace="book")),
    path("api/v1/users/", include("user.urls", namespace="user")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
