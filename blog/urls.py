from django.urls import path
from .views import PostList, PostCreate, PostDetail, PostUpdate, PostDelete, PostLike, TagPosts, CommentCreate

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('post/create/', PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('<slug:slug>/update/', PostUpdate.as_view(), name='post_update'),
    path('<slug:slug>/delete/', PostDelete.as_view(), name='post_delete'),
    path('like/<slug:slug>/', PostLike.as_view(), name='post_like'),
    path('tag/<str:tag_name>/', TagPosts.as_view(), name='tag_posts'),  # Updated to use TagPosts class-based view
    path('<slug:slug>/comment/', CommentCreate.as_view(), name='comment_create'),
]
