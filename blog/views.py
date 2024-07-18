from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import SharePostForm


def post_list(request):

    posts = Post.published.all()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)

    try:
        page = paginator.page(page_number)
    except:
        page = paginator.page(1)
    print(posts)
    return render(request, 'blog/blog.html', {
        "page": page
    })


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        created__year=year,
        created__month=month,
        created__day=day,
        slug=slug
    )

    return render(request, 'blog/blog-details.html', {
        "post": post
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
