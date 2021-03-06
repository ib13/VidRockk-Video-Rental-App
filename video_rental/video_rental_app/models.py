from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# from django.db.models.signals import post_save


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(max_length=3)
    profile_pic = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300, blank=True)
    actual_video = models.FileField()
    preview_video = models.FileField()
    price = models.PositiveIntegerField(max_length=5)

    def __str__(self):
        return self.title


class Rating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(max_length=1)
    rating_user = models.CharField(max_length=20)

    def __str__(self):
        return self.rating_user + " gave " + str(self.rating) + " rating for the video: " + str(self.video.title)


# class RatingUser(models.Model):
#     rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
#     user = models.CharField(max_length=20)

# def __str__(self):
#     return self.user


class BuyVideo(models.Model):
    video = models.ForeignKey(Video, null=True, blank=True, on_delete=models.CASCADE)
    buyer = models.CharField(max_length=20)
    rent_timestamp = models.DateTimeField(default=datetime.now)
    return_timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.buyer + " bought " + self.video.title


class Comments(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    comment = models.TextField(max_length=200)

    def __str__(self):
        return self.user+" commented on "+self.video.title

# Trigger
# def create_user(sender,**kwargs):
#     if kwargs['created']:
#         user_profile = UserInfo.objects.create(user=kwargs['instance'])
#
#
# post_save.connect(create_user,sender=User)
