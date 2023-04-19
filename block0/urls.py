from django.urls import path
from . import views


app_name = 'block0'

urlpatterns = [
    path('', views.PostListView.as_view(), name='posts'),
    path('create', views.CreatePostView.as_view(), name='create_post'),
    path('<int:pk>', views.ShowPostView.as_view(), name='show_post'),
    path('<int:pk>/edit', views.EditPostView.as_view(), name='edit_post'),
    path('<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('<int:post_id>/leave_comment', views.leave_comment, name='leave_comment'),
    path('fake', views.create_fake_posts),
    path('converter', views.exchange, name='exchange')
]
