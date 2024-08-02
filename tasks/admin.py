from django.contrib import admin

from .models import List, Group, Comment, Post

admin.site.register(List)
admin.site.register(Group)
admin.site.register(Post)
admin.site.register(Comment)
