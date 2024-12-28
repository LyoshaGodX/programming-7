from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views  # Импортируем ваше представление для регистрации

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    
    # Маршруты для аутентификации
    path("login/", auth_views.LoginView.as_view(), name="login"),  # Страница входа
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),  # Страница выхода
    path("register/", views.register, name="register"),  # Страница регистрации
]
