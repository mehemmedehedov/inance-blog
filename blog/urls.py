from django.urls import path 
from . import views 


app_name = 'blog' 

urlpatterns = [ 
    path('',views.blog,name='blog'), 
    path('add-article',views.add_article,name='add-article'), 
    path('blog/edit-article/<int:id>/',views.edit_article,name='edit-article'), 
    path('blog/delete-article/<int:pk>/',views.delete_article,name='delete-article'),
    path('blog/<int:id>/',views.blog_detail,name='blog-detail'), 
    path('search-blogs/', views.BlogSearchView.as_view(), name='search_blogs'),
    path('example/', views.example, name='example'),
 

]