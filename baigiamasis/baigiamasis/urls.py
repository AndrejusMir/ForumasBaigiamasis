"""
URL configuration for baigiamasis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import register, user_login, search_results, create_profile, edit_profile, profile_view, forum_list, thread_list, thread_detail, new_thread
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='index'),
    path('downloads/', views.download_page, name='downloads'),
    path('password_generator/<int:program_id>/', views.password_generator, name='password_generator'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('search/', search_results, name='search_results'),
    path('create_profile/', create_profile, name='create_profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/create/', views.article_create, name='article_create'),
    path('articles/approve/<int:pk>/', views.article_approve, name='article_approve'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
    path('forum/', forum_list, name='forum_list'),
    path('forum/<int:subforum_id>/', views.thread_list, name='thread_list'),
    path('forum/thread/<int:thread_id>/', thread_detail, name='thread_detail'),
    path('forum/<int:subforum_id>/new_thread/', views.new_thread, name='new_thread'),
    path('forum/thread/<int:thread_id>/new_post/', views.new_post, name='new_post'),
    path('forum/thread/post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('api/reply_to_post/', views.reply_to_post, name='reply_to_post'),
    path('api/quote_post/', views.quote_post, name='quote_post'),
    path('api/like_post/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.profile_view, name='profile_view'),
    path('api/get_likers/<int:post_id>/', views.get_likers, name='get_likers'),
    path('post/edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
