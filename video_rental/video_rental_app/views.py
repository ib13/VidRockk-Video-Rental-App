# from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Video, Rating
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm, VideoForm, UserLoginForm, RatingForm
from django.contrib.auth import login, logout, authenticate


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
        form = VideoForm(request.POST,request.FILES)
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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            password = request.POST['password']
            obj.set_password(password)
            obj.save()
            user = authenticate(username=obj.username, password=password)
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
    cont_dict = {
        'videos': videos,
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
        if request.user.is_authenticated:
            form = RatingForm()
            cont_dict = {
                'detail_view': detail_view,
                'details': details,
                'avg_rating': avg_rating,
                'form': form
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
            return redirect('detail', id)
        else:
            return redirect('detail', id)
