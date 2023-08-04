from django.contrib import admin
from .models import UserImage 
from .models import IntruderImage 
from .models import WebsiteList

# Register your models here.
admin.site.register(UserImage)
admin.site.register(IntruderImage)
admin.site.register(WebsiteList)