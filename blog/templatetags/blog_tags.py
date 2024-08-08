from django import template
from taggit.models import Tag
from django.db.models import Count
from ..models import Post

register = template.Library()


@register.inclusion_tag(name="recent_tags", filename="blog/recent_tags.html")
def get_recent_tags():
    tags = Tag.objects.annotate(
        number_of_posts=Count('taggit_taggeditem_items')).order_by('-number_of_posts')[:9]
    return {"recent_tags": tags}


@register.inclusion_tag(name="recent_posts", filename="blog/recent_posts.html")
def get_recent_posts():
    posts = Post.published.all()[:3]
    return {"recent_posts": posts}


@register.simple_tag()
def get_most_comments_posts(post_id):
    posts = Post.published.annotate(comments_count=Count(
        "comments"))
    return posts.exclude(id=post_id).order_by("-comments_count")[:2]
