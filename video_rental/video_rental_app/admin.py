from django.contrib import admin
from .models import Video, Rating, UserInfo, BuyVideo, Comments

admin.site.register(Video)
admin.site.register(Rating)
admin.site.register(UserInfo)
admin.site.register(BuyVideo)
admin.site.register(Comments)
