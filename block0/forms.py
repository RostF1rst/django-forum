from django import forms
from block0 import models


class EditPostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('title', 'content')

    title = forms.CharField(
        required=True,
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    content = forms.CharField(
        required=True,
        localize=True,
        label='',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        max_length=1000
    )
