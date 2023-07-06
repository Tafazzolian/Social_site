from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
#from base.models import Vote

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=30)
    body = models.TextField()
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.slug} - {self.updated}'

    def get_absolute_url(self):
        return reverse('account:post_detail', args=(self.id,self.slug))

    def like_count(self):
        return self.pvotes.count()

    def button_disable(self, user):
        user_like = user.uvotes.filter(post=self)
        if user_like.exists():
            return True
        return False


class Relation(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} follows {self.to_user}'