from django.urls import path
from . import views

urlpatterns = [
    path('datetime', views.date_time_test_api),
    path('random_post', views.random_post),
    path('post', views.post)
]
