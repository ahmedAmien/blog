from django.contrib import admin
from .models import Post, Comment, Replay
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_filter = ('publish', 'status', 'created', 'author')
    search_fields = ('title', 'body')
    list_display = ('title', 'slug', 'publish', 'status', 'author')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-publish', 'status')
    raw_id_fields = ('author',)
    date_hierarchy = "created"
    show_facets = admin.ShowFacets.ALWAYS


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'email', 'public')
    list_filter = ('public', 'created', 'updated')
    search_fields = ('name', 'body', 'email')
    ordering = ('-created', '-public')
    date_hierarchy = "created"
    raw_id_fields = ('post',)


class ReplayAdmin(CommentAdmin):
    list_display = ('name', 'body', 'comment', 'email', 'public')
    raw_id_fields = ('comment',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Replay, ReplayAdmin)
