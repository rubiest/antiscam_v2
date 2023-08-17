from django import forms

class SearchCreateScammerForm(forms.Form):
    phone_number = forms.CharField(
        label='Scammer Phone Number',
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True)