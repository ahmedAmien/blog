from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import SharePostForm, CommentForm
from taggit.models import Tag
from django.db.models import Count


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    if tag_slug:
        get_object_or_404(Tag, slug=tag_slug)
        posts = Post.published.filter(tags__slug=tag_slug)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    tags = Tag.objects.annotate(
        number_of_posts=Count('taggit_taggeditem_items')).order_by('-number_of_posts')[:9]

    try:
        page = paginator.page(page_number)
    except:
        page = paginator.page(1)

    return render(request, 'blog/blog.html', {
        "page": page,
        "tags": tags
    })


def post_detail(request, year, month, day, slug):
    comment_form = CommentForm
    valid = True
    post = get_object_or_404(
        Post,
        created__year=year,
        created__month=month,
        created__day=day,
        slug=slug
    )

    if request.method == 'POST':
        valid = False
        comment = request.GET.get('comment')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            valid = True
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            comment_form = CommentForm()

    related_posts = Post.objects.all().exclude(id=post.id)
    if post.tags:
        tags_ids = post.tags.values_list('id', flat=True)
        related_posts = related_posts.filter(
            tags__id__in=tags_ids)
        related_posts = related_posts.annotate(
            tags_count=Count("tags")).order_by('-tags_count')[:2]
    return render(request, 'blog/blog-details.html', {
        "post": post,
        "comment_form": comment_form,
        "valid": valid,
        "related_posts": related_posts,
    })


def post_share(request, year, month, day, slug):
    form = SharePostForm()
    post = get_object_or_404(
        Post,
        created__year=year,
        created__month=month,
        created__day=day,
        slug=slug
    )
    sent = False
    if request.method == 'POST':
        form = SharePostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            email = EmailMessage(
                subject=f"{cd['name']} ({cd['from_email']}) recommends you read {post.title}",
                body=f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comment: {cd['comment']}",
                from_email=None,
                to=(cd['to_email'],),
                cc=(cd['from_email'],)
            )
            email.send()
            sent = True

    return render(request, 'blog/share-post.html', {
        'post': post,
        'form': form,
        'sent': sent,
    })
