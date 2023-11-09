from django.urls import path, include
from . import views

urlpatterns = [
    path('posts/', views.PostListApiView.as_view())

]