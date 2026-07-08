from django.urls import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='blog_list'),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='blog_detail'),
]
