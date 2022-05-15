from django.urls import path
from .views import LoginView, LogoutView, RegisterView, UserApi, RefreshTokenView
urlpatterns = [
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('register', RegisterView.as_view()),
    path('get_user', UserApi.as_view()),
    path('get_new_token', RefreshTokenView.as_view())
]