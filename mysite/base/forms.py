from django import forms
from django.contrib.auth.models import User
from .models import Comment

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','placeholder':'Type your comment'})
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body':forms.Textarea(attrs={'class':'form-control','placeholder':'Type your comment'})
        }

class SearchForm(forms.Form):
    search = forms.CharField()