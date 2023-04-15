from django import forms


class EditPostForm(forms.Form):
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
