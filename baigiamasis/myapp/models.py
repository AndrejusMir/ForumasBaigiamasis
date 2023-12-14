from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

class AdminPanel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    birth_date = models.DateField(null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    discord = models.CharField(max_length=100, null=True, blank=True)
    skype = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def thumbnail_image(self):
        images = self.images.all()
        if images:
            return images[0].image.url
        else:
            return '/media/thumbnails/default.png'

class Image(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_images/')

    def __str__(self):
        return f"Image for {self.article.title}"


class Subforum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Thread(models.Model):
    subforum = models.ForeignKey(Subforum, related_name='threads', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.content[:20]

class Program(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.name






