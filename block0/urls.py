from django.urls import path
from . import views


app_name = 'block0'

urlpatterns = [
    path('', views.posts, name='posts'),
    path('create', views.create_post, name='create_post'),
    path('<int:post_id>', views.show_post, name='show_post'),
    path('<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('<int:post_id>/leave_comment', views.leave_comment, name='leave_comment'),
    path('fakeposts', views.faker_create_posts),
    path('converter', views.exchange, name='exchange')
]
