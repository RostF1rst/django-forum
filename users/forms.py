from django import forms


class AvatarForm(forms.Form):
    avatar = forms.ImageField(
        required=True,
        label='',
        widget=forms.FileInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
