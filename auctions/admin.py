from django.contrib import admin

from .models import Listing, UserBid, UserComment, User

# Register your models here.

admin.site.register(Listing)
admin.site.register(UserBid)
admin.site.register(UserComment)
admin.site.register(User)