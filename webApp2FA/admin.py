from django.contrib import admin
from .models import UserImage 
from .models import FailedAuthen 
from .models import WebsiteList

class WebsiteListAdmin(admin.ModelAdmin):
    list_display = ('websiteListID', 'userID', 'websiteName', 'websiteUrl', 'username', 'created_At')

class UserImageAdmin(admin.ModelAdmin):
    list_display = ('userID', 'userImage', 'uploaded_at')

class FailedAuthenAdmin(admin.ModelAdmin):
    list_display = ('FailedAuthenID', 'userID', 'FailedAuthenImage', 'uploaded_at')

# Register your models here.
admin.site.register(UserImage, UserImageAdmin)
admin.site.register(FailedAuthen, FailedAuthenAdmin)
admin.site.register(WebsiteList, WebsiteListAdmin)