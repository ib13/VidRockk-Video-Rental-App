from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# class UserInfo(models.Model):                                      #Not required
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=300, blank=True)
    actual_video = models.FileField(blank=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return str(self.video) + " : " + str(self.rating)
