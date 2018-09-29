from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('', views.PostView.as_view(), name='homePage'),
    path('about/', views.AboutTemplateView.as_view(), name='aboutPage'),
    path('create_post/', views.CreateNewPostView.as_view(), name='post_create'),
    path('post_detail/<pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post_delete/<pk>', views.DeletePostView.as_view(), name='post_delete'),
    path('post_update/<pk>', views.UpdatePostView.as_view(), name='post_update'),
    path('nopermissionwarning/',
         views.NoPermisionTemplateView.as_view(), name='nopermission'),
    path('users/<pk>/posts', views.UserPostsListView.as_view(), name='userPostsView'),
    path('post_detail/<pk>/delete',
         views.CommentDeleteView.as_view(), name='comment_delete'),
    path('post_detail/<pk>/edit',
         views.CommentEditView.as_view(), name='edit_comment'),
]
