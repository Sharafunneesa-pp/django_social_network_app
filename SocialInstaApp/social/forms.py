from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from social.models import UserProfile,Posts
class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","password1","password2"]


class LoginForm(forms.Form):
    username=forms.CharField()  
    password=forms.CharField(widget=forms.PasswordInput())

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user","followings")
        widgets={
            "dob":forms.DateInput(attrs={"class":"form-control","type":"date"})

        }


class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","image"]
