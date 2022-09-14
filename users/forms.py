from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput, help_text=None)
    email = forms.CharField(label='Email', widget=forms.EmailInput, help_text=None)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, help_text=None)

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('full_name',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomSignUpForm(CustomUserCreationForm):
    
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'username',]