from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Video, Rating, UserInfo, RatingUser
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm, VideoForm, UserLoginForm, RatingForm, UserEditForm
from django.contrib.auth import login, logout, authenticate


class UserEditView(View):
    def get(self, request):
        form = UserEditForm(instance=request.user)
        cont_dict = {
            'form': form,
        }
        return render(request, 'video_rental_app/profile_edit.html', context=cont_dict)

    def post(self, request):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            x=UserInfo.objects.get(user=obj)
            x.profile_pic=request.FILES['profile_pic']
            x.age=request.POST['age']
            obj.save()
            x.save()
            return redirect('profile_view',request.user.username)
        else:
            return redirect('edit_profile')


class ProfileView(View):
    def get(self, request, username):
        if request.user.is_authenticated:
            user = get_object_or_404(User, username=username)
            user1 = get_object_or_404(UserInfo, user=user)
            cont_dict = {
                'user1': user1,
                'user': user,
            }
        else:
            cont_dict = {}
        return render(request, 'video_rental_app/profile_view.html', context=cont_dict)


# @login_required
class VideoFormFill(View):
    def get(self, request):
        if request.user.is_authenticated:  # if user is authenticated then only make form
            form = VideoForm()
            cont_dict = {
                'form': form,
            }
        else:
            cont_dict = {}
        print("Form displayed")
        return render(request, 'video_rental_app/videoform.html', context=cont_dict)

    def post(self, request):
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            print("Valid")
            # form.save(commit=True)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect('index')
        else:
            print("Invalid")
            return redirect('videoform')


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        cont_dict = {
            'form': form
        }
        return render(request, 'video_rental_app/register.html', context=cont_dict)

    def post(self, request):
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            password = request.POST['password']
            age = request.POST['age']
            profile_pic = request.FILES['profile_pic']
            obj.set_password(password)
            obj.save()
            user = authenticate(username=obj.username, password=password)
            UserInfo.objects.create(user=user, age=age, profile_pic=profile_pic)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return redirect('register')
        else:
            return redirect('register')


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        cont_dict = {
            'form': form
        }
        return render(request, 'video_rental_app/login.html', context=cont_dict)

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            # print(username)
            password = request.POST['password']
            # print(password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')
        else:
            return redirect('login')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


def index(request):
    videos = Video.objects.all()
    video_list = []
    for i in videos:
        video_list += [i.title]
        print(video_list)
    cont_dict = {
        'videos': videos,
        'video_list': video_list,
    }
    # Video.objects.create(title='ABC',author='XYZ',description='This a video',rating=5)

    return render(request, 'video_rental_app/index.html', context=cont_dict)


class DetailsView(View):
    def get(self, request, id):
        detail_view = get_object_or_404(Video, id=id)
        # detail_view=Video.objects.get(id=id)                        #Alternative but it will not show 404
        # details=Rating.objects.get_list(video=detail_view)          #Wrong
        # details=Rating.objects.all()                                #Show all the objects
        details = Rating.objects.filter(video=detail_view)

        avg_rating = 0

        for i in details:
            avg_rating += i.rating

        if len(details):
            avg_rating = avg_rating / len(details)
        else:
            avg_rating = 'Not Rated'
        # details=details[:3]                     #Show only 3 ratings
        userrating=RatingUser.objects.filter(user=request.user.username,rating=details)
        if request.user.is_authenticated:
            form = RatingForm()
            cont_dict = {
                'detail_view': detail_view,
                'details': details,
                'avg_rating': avg_rating,
                'form': form,
                'userrating': userrating,
            }
        else:
            cont_dict = {
                'detail_view': detail_view,
                'details': details,
                'avg_rating': avg_rating,
            }

        return render(request, 'video_rental_app/detail.html', context=cont_dict)

    def post(self, request, id):
        form = RatingForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.video = Video.objects.get(id=id)
            obj.save()
            x = RatingUser.objects.create(rating=obj, user=request.user.username)
            x.save()
            return redirect('detail', id)
        else:
            return redirect('detail', id)
