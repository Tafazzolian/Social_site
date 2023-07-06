from django.shortcuts import render
from django.views import View
from account.models import Posts
from .forms import SearchForm
from django.contrib.auth.models import User

class HomePage(View):
    form_class = SearchForm
    def get(self,request):
        post = Posts.objects.all()
        if request.GET.get('search'):
            post = post.filter(body__icontains=request.GET['search'] , title__icontains=request.GET['search'])
        return render(request,'main.html',{'post':post,'search':self.form_class})

def welcome(request):
    post = Posts.objects.all()
    #user = User.objects.get(id=username)
    return render(request,'base/welcome.html',{'post':post})
