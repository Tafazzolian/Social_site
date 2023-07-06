from django.contrib import admin
from .models import Comment, Vote, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user','post','body','is_reply')
    raw_id_fields = ('user','post','reply')

admin.site.register(Comment, CommentAdmin)

admin.site.register(Vote)
admin.site.unregister(User) #we unregistered default user model to have the new customized user model using UserAdmin and Profile model


class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtendedUser(UserAdmin):
    inlines = (ProfileInLine,)

admin.site.register(User, ExtendedUser)