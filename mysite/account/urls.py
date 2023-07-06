from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('',views.RegisterView.as_view(), name='register'),
    path('login/',views.UserLoginView.as_view(), name='login'),
    path('logout/',views.UserLogoutView.as_view(), name='logout'),
    path('profile/<int:user_id>/',views.UserProfileView.as_view(), name='profile'),
    path('posts/',views.UserPostView.as_view(), name='post'),
    path('posts/<int:post_id>/<slug:post_slug>/',views.PostDetailView.as_view(), name='post_detail'),
    path('posts/delete/<int:post_id>/',views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/update/<int:post_id>/',views.PostUpdateView.as_view(), name='post_update'),
    path('posts/create/',views.PostCreateView.as_view(), name='post_create'),
    path('reset/',views.PasswordResetView.as_view(), name='reset_password'),
    path('reset/done/',views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('confirm/complete/',views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('follow/<int:user_id>',views.UserFollowView.as_view(), name='user_follow'),
    path('unfollow/<int:user_id>',views.UserUnfollowView.as_view(), name='user_unfollow'),
    path('reply/<int:post_id>/<int:comment_id>',views.CommentReplyView.as_view(),name='reply'),
    path('like/<int:post_id>/',views.PostLikeView.as_view(), name='post_like'),
    path('edit/',views.EditProfileView.as_view(),name='edit_profile')
]