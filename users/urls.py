from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='register'),
    path('settings/', views.settings, name='settings'),
    path('<int:pk>/', views.user_page, name='user_page'),
    path('fake', views.create_fake_user),
]
