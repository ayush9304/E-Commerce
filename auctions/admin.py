from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(UserBid)
admin.site.register(UserComment)
admin.site.register(User)