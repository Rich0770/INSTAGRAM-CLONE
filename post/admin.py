from django.contrib import admin

from post.models import Post, Comment, CommentLike, Like

# Register your models here.

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Like)