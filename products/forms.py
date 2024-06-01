from django import forms
from .models import Comment
from django.contrib.auth.mixins import LoginRequiredMixin


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
