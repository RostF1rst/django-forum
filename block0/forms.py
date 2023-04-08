from django import forms


class CreatePostForm(forms.Form):
    title = forms.CharField(label="Tell me what are you gonna tell me about", required=True)
    content = forms.CharField(label='', required=True, localize=True, widget=forms.Textarea)
