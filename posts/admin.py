from django.contrib import admin

from .models import Author, Category, Post, Like, UnLike, Report

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