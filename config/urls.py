from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("book.urls", namespace="book")),
    path("api/v1/users/", include("user.urls", namespace="user")),
    path("api/v1/borrowings/", include("borrowing.urls", namespace="borrowing")),
    path("api/v1/payments/", include("payment.urls", namespace="payment"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
