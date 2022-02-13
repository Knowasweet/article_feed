from django.urls import path
from .views import *

app_name = 'article_feed'

user_create = UserRegistrationView.as_view({'post': 'create'})
article = ArticleView.as_view({'post': 'create', 'get': 'list'})
article_detail = ArticleDetailView.as_view(
    {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('users/registrate', user_create, name='user_create'),
    path('articles', article, name='article'),
    path('articles/<int:pk>', article_detail, name='article_detail'),
]
