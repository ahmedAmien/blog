from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models.functions import Now
# Create your models here.


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISH)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DB', 'Draft'
        PUBLISH = 'PB', 'Publish'

    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField()
    slug = models.SlugField(max_length=250)
    publish = models.DateTimeField(db_default=Now())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT
    )

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        indexes = [
            models.Index(fields=['-publish'])
        ]
        ordering = ['-publish']

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"year": self.created.year, "month": self.created.month, "day": self.created.day, "slug": self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return self.body


class Replay(models.Model):
    comment = models.ForeignKey(
        Comment,
        related_name="replays",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=150)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return self.body
