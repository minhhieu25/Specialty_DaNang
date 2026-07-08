from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, BlogCategory

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Getting all articles filtered by the queryset
        articles = self.get_queryset()
        
        # If there is a filter, maybe don't separate featured
        category_slug = self.request.GET.get('category')
        search_query = self.request.GET.get('q')
        
        if not category_slug and not search_query:
            featured = articles.filter(is_featured=True).first()
            if not featured:
                featured = articles.first()
                
            context['featured_article'] = featured
            if featured:
                context['other_articles'] = articles.exclude(id=featured.id)[:10]
            else:
                context['other_articles'] = articles[:10]
        else:
            context['featured_article'] = None
            context['other_articles'] = articles[:10]
            
        context['categories'] = BlogCategory.objects.all()
        
        # Add current category if any
        if category_slug:
            context['current_category'] = BlogCategory.objects.filter(slug=category_slug).first()
            
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        context['related_articles'] = Article.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:3]
        return context
