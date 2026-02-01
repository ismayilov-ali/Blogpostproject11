from django.contrib import admin

from .models import Author, Category, Post, Like, UnLike, Report, Comment, PostView

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']
    
admin.site.register(UnLike)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['post', 'user']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['user__username', 'post__title', 'content']

@admin.register(PostView)
class PostViewAdmin(admin.ModelAdmin):
    list_display = ['post', 'timestamp']
    list_filter = ['timestamp', 'post']
    search_fields = ['post__title']