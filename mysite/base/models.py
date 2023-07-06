from django.db import models
from django.contrib.auth.models import User
from account.models import Posts

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ucomments')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='pcomments')
    body = models.TextField(max_length=400)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} commented {self.body[:30]}'

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='pvotes')

    def __str__(self):
        return f'{self.user} liked {self.post.slug} by {self.post.user}'


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    age = models.PositiveSmallIntegerField(default=0)
    bio = models.TextField(null=True,blank=True)
