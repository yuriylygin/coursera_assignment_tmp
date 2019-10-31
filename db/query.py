from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def clear():
    User.objects.all().delete()
    Blog.objects.all().delete()
    Topic.objects.all().delete()


def create():
    u1 = User(first_name='u1', last_name='u1')
    u2 = User(first_name='u2', last_name='u2')
    u3 = User(first_name='u3', last_name='u3')

    u1.save()
    u2.save()
    u3.save()

    blog1 = Blog(title='blog1', author=u1)
    blog2 = Blog(title='blog2', author=u1)
    blog1.save()
    blog2.save()
    blog1.subscribers.add(u1, u2)
    blog2.subscribers.add(u2)

    topic1 = Topic(title='topic1', blog=blog1, author=u1)
    topic2 = Topic(title='topic2_content', blog=blog1, author=u3, created='2017-01-01')
    topic1.save()
    topic2.save()
    topic1.likes.add(u1, u2, u3)


def edit_all():
    for user in User.objects.all():
        user.first_name = 'uu1'
        user.save()


def edit_u1_u2():
    for user in User.objects.filter(Q(first_name='u1') | Q(first_name='u2')):
        user.first_name = 'uu1'
        user.save()


def delete_u1():
    for user in User.objects.filter(first_name='u1'):
        user.delete()


def unsubscribe_u2_from_blogs():
    for user in User.objects.filter(first_name='u2'):
        for blog in Blog.objects.all():
            blog.subscribers.remove(user)


def get_topic_created_grated():
    return Topic.objects.filter(created__gt='2018-01-01')


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.all().order_by('-id')[:2]


def get_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.annotate(topic_count=Count('topic')).aggregate(avg=Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    return Blog.objects.annotate(topic_count=Count('topic')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.filter(blog__author__isnull=True)


def get_topic_that_like_all_users():
    amount_of_users = User.objects.all().aggregate(count=Count('pk'))['count']
    return Topic.objects.annotate(count_likes_user=Count('likes')).filter(count_likes_user=amount_of_users)


def get_topic_that_dont_have_like():
    return Topic.objects.annotate(count_likes_user=Count('likes')).filter(count_likes_user=0)
