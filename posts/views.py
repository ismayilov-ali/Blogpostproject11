from django.shortcuts import render, redirect
from django.db.models import Q 
from .models import Category, Post, Author, Like, Report, UnLike, Tag, Comment, PostView

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    timestamp = Post.objects.get(slug=slug).timestamp
    
    # Hər yeniləmədə oxunma sayını artır
    PostView.objects.create(post=post)
    view_count = PostView.objects.filter(post=post).count()
    
    # Commentləri əldə et
    comments = post.comments.all()
    comment_count = comments.count()
    
    # Comment formu
    if request.method == 'POST' and 'comment_submit' in request.POST:
        if request.user.is_authenticated:
            content = request.POST.get('comment_content')
            if content:
                Comment.objects.create(
                    user=request.user,
                    post=post,
                    content=content
                )
                return redirect('post', slug=slug)
    
    has_liked = False
    like_count = 0
    has_unliked = False
    unlike_count = 0
    has_reported = False
    
    if request.user.is_authenticated:
        has_liked = Like.objects.filter(user=request.user, post=post).exists()
        
    if request.user.is_authenticated:
        has_unliked = UnLike.objects.filter(user=request.user, post=post).exists()
        
    if request.user.is_authenticated:
        has_reported = Report.objects.filter(user=request.user, post=post).exists()
    
    like_count = Like.objects.filter(post=post).count()
    unlike_count = UnLike.objects.filter(post=post).count()
    
    context = {
        'post': post,
        'latest': latest,
        'has_liked': has_liked,
        'like_count': like_count,
        'has_unliked': has_unliked,
        'unlike_count': unlike_count,
        'has_reported': has_reported,
        'timestamp': timestamp,
        'view_count': view_count,
        'comments': comments,
        'comment_count': comment_count,
    }
    return render(request, 'post.html', context)

def like(request,slug):
    if not request.user.is_authenticated:
        return render(request, 'post', slug=slug)
    
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(slug=slug)
        
        like_qs = Like.objects.filter(user=user, post=post)
        
        if like_qs.exists():
            like_qs.delete()
        else:
            Like.objects.create(user=user, post=post)
    
    return redirect('post', slug=slug)

def unlike(request,slug):
    if not request.user.is_authenticated:
        return render(request, 'post', slug=slug)
    
    if request.method == "POST":
        user = request.user
        post = Post.objects.get(slug=slug)
        
        unlike_qs = UnLike.objects.filter(user=user, post=post)
        
        if unlike_qs.exists():
            unlike_qs.delete()
        else:
            UnLike.objects.create(user=user, post=post)
    
    return redirect('post', slug=slug)

def about (request):
    return render(request, 'about_page.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'object_list': queryset
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)

def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)

def report(request,slug):
    if not request.user.is_authenticated:
        return render(request, 'post', slug=slug)
    
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(slug=slug)
        
        report_qs = Report.objects.filter(user=user, post=post)
        
        if report_qs.exists():
            report_qs.delete()
        else:
            Report.objects.create(user=user, post=post)
            
    return redirect('post', slug=slug)
    
def taglist(request, slug):
    tag = Tag.objects.get(slug=slug)
    posts = Post.objects.filter(tags__in=[tag])
    
    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request, 'tag_list.html', context)

def delete_comment(request, comment_id):
    """Comment silmə funksiyası"""
    if not request.user.is_authenticated:
        return redirect('homepage')
    
    try:
        comment = Comment.objects.get(id=comment_id)
        if comment.user == request.user or request.user.is_staff:
            post_slug = comment.post.slug
            comment.delete()
            return redirect('post', slug=post_slug)
    except Comment.DoesNotExist:
        pass
    
    return redirect('homepage')