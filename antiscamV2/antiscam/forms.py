from django import forms
from .models import CustomUser

class SearchCreateScammerForm(forms.Form):
    phone_number = forms.CharField(
        label='Scammer Phone Number',
        max_length=13,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Comment/Review',
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        required=True
    )

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'profile_picture']