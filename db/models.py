from django.utils import timezone

from django.db import models


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id) + ',' + self.first_name + ',' + self.last_name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now)

    subscribers = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return str(self.id) + ',' + self.title + ',' + str(self.author.id)


class Topic(models.Model):
    title = models.CharField(max_length=255)
    blog = models.ForeignKey(Blog)
    author = models.ForeignKey(User)
    created = models.DateTimeField(default=timezone.now)

    likes = models.ManyToManyField(User, related_name='likes')

    def __str__(self):
        return str(self.id) + ',' + self.title + ',' + str(self.blog.id) + ',' \
               + str(self.author.id) + ',' + str(self.created) + ',' + str(self.likes)


class Publication(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    class Mata:
        ordering = ('headline',)

    def __str__(self):
        return self.headline