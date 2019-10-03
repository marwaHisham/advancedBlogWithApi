from django.contrib import admin
from posts.models import Post
# Register your models here.


class PostModelAdmin(admin.ModelAdmin):
    list_display = ( 'title','updated', 'timestamp')
    list_filter = ('updated', 'timestamp')
    list_display_links  = ['updated']
    search_fields=['title']
    list_editable=["title"]

    class Meta:
        model = Post
        
admin.site.register(Post,PostModelAdmin)
