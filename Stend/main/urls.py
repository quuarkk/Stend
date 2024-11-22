from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/latest-post/', views.get_latest_post, name='get_latest_post'),
    path('', views.index),
    path('about', views.about)
]