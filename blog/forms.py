from django import forms


class SharePostForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Your Name',
                   'name': 'author', 'id': 'author'}
        ),
    )
    from_email = forms.EmailField(
        label='Your Email Address',
        widget=forms.EmailInput(
            attrs={'placeholder': 'your-real-email@example.com',
                   'name': 'from_email', 'id': 'from_email'}
        ),
    )
    to_email = forms.EmailField(
        label='Recipient’s Email Address',
        widget=forms.EmailInput(
            attrs={'placeholder': 'recipient-real-email@example.com',
                   'name': 'to_email', 'id': 'to_email'}
        ),
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'id': 'comment',
                'name': 'comment',
                'cols': 45,
                'rows': 8,
                'maxlength': 65525,
                'placeholder': 'Comment',
                'required': False,
            }
        )
    )
