from .models import Video
from django import forms
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class Video_form(forms.ModelForm):
    class Meta:
        model=Video
        fields=("caption","video")