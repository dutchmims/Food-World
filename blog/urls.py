from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='post_delete'),
    path('like/<slug:slug>/', views.PostLike.as_view(), name='post_like'),
    path('tag/<str:tag_name>/', views.tag_posts, name='tag_posts'),
]
