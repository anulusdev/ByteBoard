from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ['title', 'content', 'author', 'date_posted', 'status']
	list_filter = ['status', 'date_posted', 'author']
	prepopulated_fields = {'slug' : ('title',)}
	raw_id_fields = ['author']