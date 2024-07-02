from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Article,Author,Tag
from .forms import ArticleForm
from django.core.paginator import Paginator
from django.db.models import F
from django.views.generic import ListView
from .models import *

# Create your views here.

def blog(request):
    articles=Article.objects.all() #SELECT * FROM blog_article;
    author_username=request.GET.get('author')
    authors=Author.objects.all()
    tags=Tag.objects.all()
    tag_title=request.GET.get('tag')
    page_number=int(request.GET.get('page', 1))
    if author_username:
        articles=articles.filter(author__user__username=author_username)
    if tag_title:
        articles=articles.filter(tags__title=tag_title)
    paginator=Paginator(articles, 1)
    page=paginator.page(page_number)
    articles=page.object_list

    return render(request,'blog.html',context={'articles':articles,'authors':authors,'tags':tags, 'paginator':paginator,'page':page})

def blog_detail(request,id):
    article=Article.objects.get(id=id)
    return render(request,'blog-detail.html',context={'article':article})

def add_article(request):
    if request.method == 'POST':
        data = request.POST.copy()
        form = ArticleForm(data=data, files=request.FILES)
        if form.is_valid():
            form.save(request.user.author)
            return redirect('blog:add-article')
        return render(request, 'add-article.html', {'form': form})
    else:
        form = ArticleForm()
        return render(request, 'add-article.html', {'form': form})

def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    if article.author.user != request.user:
        raise PermissionDenied()
    if request.method == 'POST':
        data = request.POST.copy()
        data['author'] = request.user.author.id
        form = ArticleForm(data=data, files=request.FILES, instance=article)
        if form.is_valid():
            form.save(request.user.author)
            return redirect('blog:add-article') 
        return render(request, 'add-article.html', {'form': form})
    else:
        form = ArticleForm(instance=article)
        return render(request, 'add-article.html', {'form': form})


def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if article.author.user != request.user:
        raise PermissionDenied()
    article.delete()
    return redirect('blog:blog',pk=article.pk) 

class BlogSearchView(ListView):
    model = blog 
    template_object_name = 'blog.html'
    context_object_name = 'post'

    def get_queryset(self):
        query = self.request.GET.get('q')  
        return blog.objects.filter(title__icontains=query).order_by('-created_at')

    
def example(request):
    users = [
        {'name':'alice','profession': 'Software Engineer', 'age': 30},
        {'name':'bob','profession': 'Data Analyst', 'age': 28},
        {'name':'charlie','profession': 'Designer', 'age': 32},
        {'name':'david','profession': 'Teacher', 'age': 35},
       ]
    return render(request, 'example.html',context={'users':users})

