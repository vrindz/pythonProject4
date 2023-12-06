from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='Home'),
    path('index/', views.index, name="index"),
    path('search/', views.search_songs, name='search_songs'),
    path('register',views.register,name='register'),
    path('login_user',views.login_user,name='login_user'),
    path('logout',views.logout,name='logout'),


]