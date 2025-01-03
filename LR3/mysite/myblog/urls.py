from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),  # Подключаем маршруты приложения blog
    path("accounts/", include("allauth.urls")),
    path('poll_analytics/', include('poll_analytics.urls')),  
]
