from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View
from .models import Video, Rating, UserInfo, BuyVideo, Comments
from django.shortcuts import get_object_or_404
from .forms import UserRegisterForm, VideoForm, UserLoginForm, RatingForm, UserEditForm, BuyForm, VideoEditForm, \
    CommentForm
from django.contrib.auth import login, logout, authenticate


class DeleteVideo(View):
    def post(self, request, id):
        video = get_object_or_404(Video, id=id)
        if request.user == video.user:
            video.delete()
            return redirect('index')
        else:
            raise Http404()


class EditVideo(View):
    def get(self, request, id):
        video = get_object_or_404(Video, id=id)
        form = VideoEditForm(initial={
            'title': video.title,
            'description': video.description,
            'price': video.price,
        })
        cont_dict = {
            'form': form,
            'video': video,
        }
        return render(request, 'video_rental_app/edit_video.html', context=cont_dict)

    def post(self, request, id):
        form = VideoEditForm(request.POST)
        video = get_object_or_404(Video, id=id)
        cont_dict = {
            'form': form,
            'video': video,
        }
        if form.is_valid():

            video.price = request.POST['price']
            video.description = request.POST['description']
            video.title = request.POST['title']
            video.save()
            return redirect('detail', id)
        else:
            return render(request, 'video_rental_app/edit_video.html', context=cont_dict)


class CommentPost(View):
    def post(self, request, id):
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            obj = commentform.save(commit=False)
            obj.video = get_object_or_404(Video, id=id)
            obj.user = request.user.username
            obj.save()
            return redirect('detail', id)
        else:
            return redirect('detail', id)


class BuyPost(View):
    def post(self, request, id):
        buyform = BuyForm(request.POST)
        if buyform.is_valid():
            obj = buyform.save(commit=False)
            obj.video = Video.objects.get(id=id)
            obj.buyer = request.user.username
            obj.return_timestamp = obj.rent_timestamp + timedelta(minutes=2)
            obj.save()
            return redirect('detail', id)
        else:
            return redirect('detail', id)


class RatingPost(View):
    def post(self, request, id):
        form = RatingForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.video = Video.objects.get(id=id)
            obj.rating_user = request.user.username
            obj.save()
            return redirect('detail', id)
        else:
            return redirect('detail', id)


class BoughtList(View):
    def get(self, request):
        bought = BuyVideo.objects.filter(buyer=request.user.username).order_by('-id')
        cont_dict = {
            'bought': bought,
            'timezone':timezone.now(),
        }
        return render(request, 'video_rental_app/boughtlist.html', context=cont_dict)


class BuyList(View):
    def get(self, request):
        video = Video.objects.filter(user=request.user).order_by('-id')
        buyfinal = []
        for i in video:
            buy = BuyVideo.objects.filter(video=i)
            buyfinal.append(buy)

        money = 0
        for i in buyfinal:
            for j in i:
                money += j.video.price
        cont_dict = {
            'buy': buyfinal,
            'money': money,
            'timezone': timezone.now(),
        }
        return render(request, 'video_rental_app/buylist.html', context=cont_dict)


class UserEditView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = UserEditForm(instance=request.user, initial={
                'age': UserInfo.objects.get(user=request.user).age,
                'profile_pic': UserInfo.objects.get(user=request.user).profile_pic})
            cont_dict = {
                'form': form,
            }
        else:
            cont_dict = {}
        return render(request, 'video_rental_app/profile_edit.html', context=cont_dict)

    def post(self, request):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            obj = form.save(commit=False)
            x = UserInfo.objects.get(user=obj)
            x.profile_pic = request.FILES['profile_pic']
            x.age = request.POST['age']
            obj.save()
            x.save()
            return redirect('profile_view', request.user.username)
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
        cont_dict = {
            'form': form,
        }
        if form.is_valid():
            print("Valid")
            # form.save(commit=True)
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return redirect('detail', obj.id)
        else:
            print("Invalid")
            return render(request, 'video_rental_app/videoform.html', context=cont_dict)


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        cont_dict = {
            'form': form
        }
        return render(request, 'video_rental_app/register.html', context=cont_dict)

    def post(self, request):
        form = UserRegisterForm(request.POST, request.FILES)
        cont_dict = {
            'form': form
        }
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
                return render(request, 'video_rental_app/register.html', context=cont_dict)
        else:
            return render(request, 'video_rental_app/register.html', context=cont_dict)


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        cont_dict = {
            'form': form
        }
        return render(request, 'video_rental_app/login.html', context=cont_dict)

    def post(self, request):
        form = UserLoginForm(request.POST)
        cont_dict = {
            'form': form,
        }
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'video_rental_app/login.html', context=cont_dict)
        else:
            return render(request, 'video_rental_app/login.html', context=cont_dict)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


def index(request):
    videos = Video.objects.all()
    video_list = []
    for i in videos:
        video_list += [i.title]
        # print(video_list)
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
        user_detail = Rating.objects.filter(video=detail_view, rating_user=request.user.username)
        buy = BuyVideo.objects.filter(buyer=request.user.username, video=detail_view)
        comments = Comments.objects.filter(video=detail_view).order_by('-id')

        f1 = 1
        for i in buy:
            if i.return_timestamp > timezone.now():
                print(timezone.now())
                f1 = 0

        if f1 == 1:
            buy = 0

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
            buyform = BuyForm()
            commentform = CommentForm()
            cont_dict = {
                'detail_view': detail_view,
                'details': details,
                'avg_rating': avg_rating,
                'form': form,
                'buyform': buyform,
                'buy': buy,
                'user_detail': user_detail,
                'commentform': commentform,
                'comments': comments,
            }
        else:
            cont_dict = {
                'detail_view': detail_view,
                'details': details,
                'avg_rating': avg_rating,
                'buy': buy,
                'comments': comments,
            }

        return render(request, 'video_rental_app/detail.html', context=cont_dict)
