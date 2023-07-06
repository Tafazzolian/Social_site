from django.contrib import admin
from .models import Posts
from .models import Relation

#@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
        list_display = ('user','title','created')
        search_fields = ('body','user')
        list_filter = ('updated','created')
        prepopulated_fields = {'slug':('title',)}
        raw_id_fields = ('user',)
        pass
admin.site.register(Posts, PostsAdmin)

admin.site.register(Relation)