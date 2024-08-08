from django.urls import path
from . import views


app_name = 'blog'


urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('tags/<slug:tag_slug>', views.post_list, name='tag-post-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',
         views.post_detail, name="post_detail"),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/share',
         views.post_share, name="post_share"),
]
