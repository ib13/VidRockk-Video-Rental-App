from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('videos/<int:id>', views.DetailsView.as_view(), name='detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('videoform/', views.VideoFormFill.as_view(), name='videoform'),
    path('profile/<slug:username>',views.ProfileView.as_view(),name='profile_view'),
    path('editprofile/',views.UserEditView.as_view(),name='edit_profile'),
    path('buylist/',views.BuyList.as_view(),name='buylist'),
    path('boughtlist/',views.BoughtList.as_view(),name='boughtlist'),
    path('post1/<int:id>',views.RatingPost.as_view(),name='post1'),
    path('post2/<int:id>',views.BuyPost.as_view(),name='post2'),
    path('video_edit/<int:id>',views.EditVideo.as_view(),name='editvideo'),
    path('delete_video/<int:id>', views.DeleteVideo.as_view(),name='deletevideo'),
    path('post3/<int:id>',views.CommentPost.as_view(),name='post3'),
]