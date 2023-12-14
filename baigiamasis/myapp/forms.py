from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Article, Image, Profile, Thread, Post

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2011)))

    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'twitter', 'discord', 'skype', 'telegram', 'instagram', 'facebook', 'website', 'gender', 'country']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Image
        fields = ['image']

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
