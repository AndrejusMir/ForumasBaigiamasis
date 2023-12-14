from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Profile, Article, Image, Thread, Post, Subforum, Program
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, ProfileForm
from .forms import ArticleForm, ImageForm, ThreadForm, PostForm
from django.forms import modelformset_factory
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.models import User
import json
from .models import Post
from django.contrib import messages
import bleach
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from django.utils.safestring import SafeString
from django.core.paginator import Paginator



programs = [
    {
        'id': 1,
        'name': 'Password Generator',
        'date': 'Nov 12',
        'description': 'A simple App for generating passwords for every website.',
        'images/brain.png': 'path/to/thumbnail1.jpg',
    },
]

def home(request):
    return render(request, 'index.html')

def download_page(request):
    program = Program.objects.first()
    return render(request, 'downloads.html', {'program': program})

def password_generator(request, program_id):
    program = Program.objects.get(pk=program_id)
    return render(request, 'password_generator.html', {'program': program})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            pass
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def search_results(request):
    query = request.GET.get('query', '')
    return render(request, 'search_results.html', {'results': results})

def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_detail')
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if created:
        profile.save()
    return render(request, 'profile.html', {'profile': profile})

def article_create(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=5)
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if article_form.is_valid() and formset.is_valid():
            article = article_form.save(commit=False)
            article.author = request.user
            article.save()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Image(article=article, image=image)
                    photo.save()
            return redirect('article_list')
    else:
        article_form = ArticleForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'article_create.html', {'article_form': article_form, 'formset': formset})

@staff_member_required
def article_approve(request, pk):
    article = Article.objects.get(pk=pk)
    article.approved = True
    article.save()
    return redirect('article_list')

def article_list(request):
    articles_list = Article.objects.filter(approved=True).order_by('-published_date')
    paginator = Paginator(articles_list, 4)

    page_number = request.GET.get('page')
    articles = paginator.get_page(page_number)

    return render(request, 'article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})

def forum_list(request):
    subforums = Subforum.objects.all()
    return render(request, 'forum_list.html', {'subforums': subforums})

def thread_list(request, subforum_id):
    subforum = get_object_or_404(Subforum, id=subforum_id)
    threads = subforum.threads.annotate(posts_count=Count('posts')).all()
    return render(request, 'thread_list.html', {'subforum': subforum, 'threads': threads})

def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)
    posts = thread.posts.all()
    return render(request, 'thread_detail.html', {'thread': thread, 'posts': posts})


def new_thread(request, subforum_id):
    subforum = get_object_or_404(Subforum, pk=subforum_id)
    if request.method == 'POST':
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            thread = thread_form.save(commit=False)
            thread.subforum = subforum
            thread.author = request.user
            thread.save()

            post = post_form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()

            return redirect('thread_detail', thread_id=thread.pk)
    else:
        thread_form = ThreadForm()
        post_form = PostForm()

    return render(request, 'new_thread.html', {
        'subforum': subforum,
        'thread_form': thread_form,
        'post_form': post_form
    })


@login_required
@require_POST
def new_post(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    data = json.loads(request.body)
    content = data.get('content')
    clean_content = bleach.clean(
        content,
        tags=['p', 'strong', 'em', 'blockquote', 'ul', 'li', 'ol', 'br'],
        attributes=['href', 'style'],
        strip=True
    )
    if not clean_content or clean_content.isspace():
        return JsonResponse({'success': False, 'error': 'The post content cannot be empty.'}, status=400)

    post = Post(thread=thread, author=request.user, content=clean_content)
    post.save()

    return JsonResponse({'success': True, 'message': 'Post created successfully'})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author and not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', thread_id=post.thread.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})

def forum_list(request):
    subforums = Subforum.objects.annotate(
        threads_count=Count('threads'),
        posts_count=Count('threads__posts')
    )
    return render(request, 'forum_list.html', {'subforums': subforums})


@require_POST
@login_required
def like_post(request):
    try:
        data = json.loads(request.body)
        post_id = data['postId']
        post = Post.objects.get(id=post_id)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            action = 'unliked'
        else:
            post.likes.add(request.user)
            action = 'liked'

        return JsonResponse({
            'success': True,
            'new_likes_count': post.likes.count(),
            'action': action
        })
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@require_POST
@login_required
def reply_to_post(request):

    post_id = request.POST.get('postId')
    content = request.POST.get('content')


    parent_post = Post.objects.get(id=post_id)
    thread = parent_post.thread


    reply_post = Post(
        thread=thread,
        author=request.user,
        content=content
    )
    reply_post.save()

    # You might want to redirect to the thread detail page after the reply
    return JsonResponse({'success': True, 'message': 'Reply posted successfully'})

@csrf_exempt
@require_POST
@login_required
def quote_post(request):
    post_id = request.POST.get('postId')
    content = request.POST.get('content')

    quoted_post = Post.objects.get(id=post_id)
    thread = quoted_post.thread

    quote_content = f"Quoted from {quoted_post.author.username}: \"{quoted_post.content}\" \n\n {content}"

    new_post = Post(
        thread=thread,
        author=request.user,
        content=quote_content
    )
    new_post.save()

    return JsonResponse({'success': True, 'message': 'Post quoted successfully'})

@login_required
def profile_view(request, username=None):
    if username is None:
        user = request.user
        template = 'profile.html'
    else:
        user = get_object_or_404(User, username=username)
        template = 'profile_view.html'

    return render(request, template, {'profile_user': user})

@login_required
def get_likers(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    likers = post.likes.all()
    likers_usernames = [user.username for user in likers]
    return JsonResponse({'success': True, 'likers': likers_usernames})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('new_content')
        post.content = new_content
        post.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        # Handle post deletion logic here
        post.delete()
        messages.success(request, 'Post deleted successfully.')
        return redirect('thread_detail', thread_id=post.thread.id)

    return render(request, 'delete_post.html', {'post': post})

def thumbnail_image(self):
    images = self.images.all()  # Correctly using the related_name 'images'
    if images:
        return images[0].image.url
    else:
        return '/media/thumbnails/default.png'

