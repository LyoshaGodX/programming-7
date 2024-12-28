from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/new/", views.post_new, name="post_new"),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),

    # Страница входа
    path('login/', views.login_view, name='login'),

    # Страница регистрации
    path('register/', views.register, name='register'),

    # Страница выхода
    path('logout/', views.logout_view, name='logout'),
]
