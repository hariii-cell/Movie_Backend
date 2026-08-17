from django.urls import path

from .views import (
    current_user,
    home,
    login_user,
    logout_user,
    media_detail,
    media_list,
    register_user,
)

urlpatterns = [
    path('', home, name='home'),
    path('api/user/', current_user, name='current-user'),
    path('api/register/', register_user, name='register-user'),
    path('api/login/', login_user, name='login-user'),
    path('api/logout/', logout_user, name='logout-user'),
    path('api/media/', media_list, name='media-list'),
    path('api/media/<int:pk>/', media_detail, name='media-detail'),
]
