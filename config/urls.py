from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/books/", include("book.urls", namespace="book")),
    path("api/v1/users/", include("user.urls", namespace="user")),
    path("api/v1/borrowings/", include("borrowing.urls", namespace="borrowing")),
    path("api/v1/payments/", include("payment.urls", namespace="payment")),
    path("api/v1/doc/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/doc/swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/v1/doc/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
