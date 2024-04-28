from django.contrib import admin
from .models import Post, Category, Comment, ReplyComment, Category
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'slug']
    prepopulated_fields = {'slug': ('title', )}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}


class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'author']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ReplyComment, ReplyCommentAdmin)

