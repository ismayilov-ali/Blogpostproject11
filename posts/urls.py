from . import views
from django.urls import path

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('post/<slug>/', views.post, name='post'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('postlist/<slug>/', views.postlist, name='postlist'), 
    path('posts/', views.allposts, name='allposts'),
    path('like/<slug>/', views.like, name='like-post'),
    path('report/<slug>/', views.report, name='report-post'),
    path('unlike/<slug>/', views.unlike, name='unlike-post'),
    path('taglist/<slug>/', views.taglist, name='taglist'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),
]