from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Video, Rating, BuyVideo, Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']


class VideoEditForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'price', 'description']
        labels = {
            'price': 'Price(in Rs.)',
        }


class BuyForm(forms.ModelForm):
    class Meta:
        model = BuyVideo
        fields = []


class UserEditForm(UserChangeForm):
    age = forms.IntegerField()
    profile_pic = forms.ImageField(required=False)
    password = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        help_texts = {
            'password': None,
        }


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        # fields = '__all__'
        fields = ['title', 'description', 'preview_video', 'actual_video', 'price']
        labels = {
            'price': 'Price(in Rs.)',
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()
    profile_pic = forms.ImageField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'age', 'profile_pic']
        help_texts = {
            'username': None,
        }


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
