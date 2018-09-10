from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.DetailsView.as_view(), name='detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('videoform/', views.VideoFormFill.as_view(), name='videoform'),
    # path('<int:id>/rating', views.detail, name='rating'),
    path('profile/<slug:username>',views.ProfileView.as_view(),name='profile_view'),
    path('editprofile/',views.UserEditView.as_view(),name='edit_profile'),
]