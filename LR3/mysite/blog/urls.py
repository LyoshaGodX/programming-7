from django.urls import path
from . import views

urlpatterns = [
    # Маршруты для постов
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/new/", views.post_new, name="post_new"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),

    # Маршруты для авторизации
    path("login/", views.login_view, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Маршруты для опросов
    path("polls/", views.poll_list, name="poll_list"),
    path("polls/<int:pk>/vote/", views.poll_vote, name="poll_vote"),  # Роут для голосования
    path("polls/<int:pk>/results/", views.poll_results, name="poll_results"),  # Роут для просмотра результатов
    path("polls/new/", views.poll_new, name="poll_new"),
    path("polls/<int:pk>/edit/", views.poll_edit, name="poll_edit"),
    path("polls/<int:pk>/delete/", views.poll_delete, name="poll_delete"),
]
