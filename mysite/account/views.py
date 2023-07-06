from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegisterForm, UserLoginForm, PostUpdateForm, EditProfileForm
from .models import Posts, Relation
from base.models import Comment, Vote, Profile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.utils.text import slugify
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from base.forms import CommentCreateForm, CommentReplyForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class RegisterView(View): #user registration
    form_class = RegisterForm
    template_name = 'account/register.html'
    def get(self,request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            #Profile.objects.create(user=user)
            messages.success(request, 'Registration complete')
            #return render(request, self.template_name, {'form':form})
            return redirect('base:home')
        else:
            messages.error(request,'Sth went wrong!',)
            return render(request, self.template_name, {'form':form})
            #return redirect('account:register')


class UserLoginView(View): #user login
    form_class = UserLoginForm
    template_name = 'account/login.html'
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request,'already logged in')
            return redirect('base:home')
        else:
            return super() .dispatch(request, *args,**kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user:
                login(request,user)
                messages.success(request,'welcome!')
                if self.next:
                    return redirect(self.next)
                return redirect('base:home')
            else:
                messages.error(request, 'username or password is wrong!')
                return render(request, self.template_name, {'form':form})


class UserLogoutView(LoginRequiredMixin, View): #user Logout
    AccessMixin.login_url = 'account:login'
    def get(self, request):
        logout(request)
        messages.success(request,'Logged out')
        return redirect('base:home')


class UserProfileView(LoginRequiredMixin, View): #user profile and his posts
    def get(self, request, user_id):
        is_following = False
        user = get_object_or_404(User, id=user_id)
        posts = user.posts.all() #the 'posts' used here is the related name in the model
        #posts = Posts.objects.filter(user=user)
        relation = Relation.objects.filter(from_user = request.user , to_user = user)
        if relation.exists():
            is_following = True
        return render(request,'account/profile.html',{'user':user , 'posts':posts,'is_following':is_following})


class UserPostView(View): #list of all posts
    def get(self,request):
        post = Posts.objects.all()
        #post = Posts.objects.order_by('created')
        return render(request, 'account/post.html',{'post':post})


class PostDetailView(View): #sigle post view
    form_class = CommentCreateForm
    form_class2 = CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Posts, pk=kwargs['post_id'], slug=kwargs['post_slug'])  #post = Posts.objects.get(id=post_id,slug=post_slug)
        return super().setup(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        can_like = False
        if request.user.is_authenticated and self.post_instance.button_disable(request.user):
            can_like=True
        comment = self.post_instance.pcomments.filter(is_reply=False)
        return render(request, 'account/detail.html', {'post':self.post_instance,'comments':comment,'form':self.form_class,'form2':self.form_class2,'can_like':can_like})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request,'comment sent successfully', 'success')
            return redirect('account:post_detail', *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, View): #deleting posts
    def get(self, request, post_id):
        post = get_object_or_404(Posts, id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success (request,'post deleted','success')
        else:
            messages.error(request,'you dont own this post','danger')
        return redirect('base:home')


class PostUpdateView(LoginRequiredMixin, View): #updating existing posts
    form_calss = PostUpdateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Posts, id=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if post.user.id != request.user.id:
            messages.error(request, 'u dont own this post', 'danger')
            return redirect('base:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self,request, *args, **kwargs):
        post = self.post_instance
        form = self.form_calss(instance=post)
        return render(request, 'account/update.html', {'form':form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_calss(request.POST, instance=post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.slug = slugify(form.cleaned_data['title'][:30])
            updated_post.save()
            messages.success(request,'update success','success')
            return redirect('account:post_detail' ,post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View): #creating posts
    form_class = PostUpdateForm
    def get(self, request):
        form = self.form_class
        return render(request, 'account/create.html',{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'])
            new_post.user = request.user
            new_post.save()
            messages.success(request,'post created successfuly','success')
            return redirect('account:post')


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('account:password_reset_done')
    email_template_name = 'account/password_reset_email.html'

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('account:password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class UserFollowView(LoginRequiredMixin, View): #follow
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user = request.user,to_user=user)
        if relation.exists():
            messages.error(request,'you are already following this user','danger')
        else:
            #Relation.objects.create(from_user=request.user, to_user=user)
            Relation(from_user=request.user, to_user=user).save()
            messages.success(request,'you are now following this user','success')
        return redirect('account:profile',user.id)


class UserUnfollowView(LoginRequiredMixin, View): #unfollow
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        if relation.exists():
            relation.delete()
            messages.success(request, 'unfollow successful', 'success')
        else:
            messages.error(request, 'you are not following this user', 'danger')
        return redirect('account:profile', user.id)


class CommentReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm
    def post(self,request,post_id,comment_id):
        comment = get_object_or_404(Comment,id=comment_id)
        post = get_object_or_404(Posts, id = post_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request,'replied successfuly','success')
        return redirect('account:post_detail',post.id,post.slug)


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Posts,id=post_id)
        like = Vote.objects.filter(post= post , user = request.user)

        if like.exists():
            messages.error(request,'already liked','danger')
        else:
            Vote.objects.create(post=post, user= request.user)
            messages.success(request,'liked successfuly','success')
        return redirect('account:post_detail', post.id, post.slug)


class EditProfileView(LoginRequiredMixin,View):
    form_class = EditProfileForm

    def get(self,request):
        form = self.form_class(instance=request.user.profile,initial={'email':request.user.email})
        return render(request, 'account/edit_profile.html',{'form':form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request,'profile updated','success')
        return redirect('account:profile',request.user.id)
