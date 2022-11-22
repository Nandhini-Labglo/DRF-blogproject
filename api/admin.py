from django.contrib import admin

from .models import Post, Comment

# Register your models here.


class Postadmin(admin.ModelAdmin):
    list_display = ["id", "title", "description", "body",
                    "user", "image", "created_at", "updated_at"]


admin.site.register(Post, Postadmin)


class Commentadmin(admin.ModelAdmin):
    list_display = ["id", "post", "body", "user", "created_at", "updated_at"]


admin.site.register(Comment, Commentadmin)
