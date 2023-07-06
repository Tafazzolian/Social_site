from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Posts
from base.models import Profile

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3 , required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'user@email.com'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Your Pass'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Pass'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email) . exists()
        if user:
            raise ValidationError('Email already taken!')
        else:
            return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username) . exists()
        if user:
            raise ValidationError('Username already taken!')
        else:
            return username

    def clean(self):
        cleaned_data = super() . clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords dont match')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('title','body',)

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ('age','bio')