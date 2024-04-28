from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, ReplyComment, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request, category_slug=None):
    posts = Post.objects.order_by('-date_posted')
    if category_slug:
        print(category_slug)
        category = Category.objects.get(slug=category_slug)
        posts = Post.objects.filter(category=category).order_by('-date_posted')
    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context)


@login_required
def post_details(request, post_slug, usn=None):
    post = get_object_or_404(Post, slug=post_slug)
    user = request.user
    comments = post.comments.order_by('-date_posted').prefetch_related('replies')
    context = {
        'post': post,
        'user': user,
        'comments': comments,
    }
    return render(request, 'post_details.html', context=context)


@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        if not title or not content:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'post_form.html')

        user = request.user
        post = Post.objects.create(title=title, content=content, author=user, category=category)
        messages.success(request, "Post created successfully.")
        return redirect('home')
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'post_form.html', context=context)


@login_required
def update_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title or not content:
            messages.error(request, "Please fill in all required fields.")
            return render(request, 'update_form.html', {'post': post})

        Post.objects.filter(pk=post_id).update(title=title, content=content)
        messages.success(request, "Post updated successfully.")
        return redirect('home')
    return render(request, 'update_form.html', {'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('home')
    return render(request, 'post_confirm_delete.html', {'post': post})


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content', '').strip()
        if content:
            comment = Comment.objects.create(author=user, post=post, content=content)
    return redirect('post_details', post_slug=post.slug, usn=post.author.usn)


def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post = get_object_or_404(Post, pk=post_id)
    comment.delete()
    return redirect('post_details', post_slug=post.slug, usn=post.author.usn)


def add_reply(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id )
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        user = request.user
        content = request.POST.get('content', '').strip()
        if content:
            reply = ReplyComment.objects.create(author=user, comment=comment, content=content)
    return redirect('post_details', post_slug=post.slug, usn=post.author.usn)


def delete_reply(request, post_id, reply_id):

    post = get_object_or_404(Post, pk=post_id)
    reply = ReplyComment.objects.get(pk=reply_id)
    reply.delete()
    return redirect('post_details', post_slug=post.slug, usn=post.author.usn)


