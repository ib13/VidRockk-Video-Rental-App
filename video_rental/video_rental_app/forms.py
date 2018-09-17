from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Video, Rating, BuyVideo, Comments


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']


class VideoEditForm(forms.ModelForm):
    price = forms.IntegerField(min_value=0, max_value=99999)

    class Meta:
        model = Video
        fields = ['title', 'price', 'description']
        labels = {
            'price': 'Price(in Rs.)',
        }

    def clean_price(self):                      #called when .is_valid() is called
        data = self.cleaned_data['price']
        if data < 0:
            raise forms.ValidationError('price should be greater than 0')
        return data


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
    price = forms.IntegerField(min_value=0, max_value=99999)

    class Meta:
        model = Video
        # fields = '__all__'
        fields = ['title', 'description', 'preview_video', 'actual_video', 'price']
        labels = {
            'price': 'Price(in Rs.)',
        }

    def clean_price(self):
        data = self.cleaned_data['price']
        if data < 0:
            raise forms.ValidationError('price should be greater than 0')
        return data


class RatingForm(forms.ModelForm):
    STATUS_CHOICES = (
        (1, ("1")),
        (2, ("2")),
        (3, ("3")),
        (4, ("4")),
        (5, ("5")),
    )
    rating = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Rating
        fields = ['rating']

    # def clean_rating(self):
    #     data = int(self.cleaned_data['rating'])
    #     if data > 5 or data < 0:
    #         raise forms.ValidationError('rating should be between 0 t0 5')
    #     return data


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()
    profile_pic = forms.ImageField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'age', 'profile_pic', 'password']
        help_texts = {
            'username': None,
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if not password == confirm_password:
            raise forms.ValidationError('Password and Confirm Password are different')
        if len(password) < 4:
            raise forms.ValidationError('Password should have 4 characters')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data['username']
        password = cleaned_data['password']
        if not User.objects.filter(username=username):
            raise forms.ValidationError('User not registered')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Password not valid')
