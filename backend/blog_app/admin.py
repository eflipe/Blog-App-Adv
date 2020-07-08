from django.contrib import admin
from blog_app.models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ("title", "update", "timestamp")

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)
