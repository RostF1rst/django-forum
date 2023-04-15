from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('<int:user_id>/', views.user_page, name='user_page'),
    path('fake', views.create_fake_user)
]
