from django.db import models
from django.contrib.auth.models import User

class UserImage(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    userImage = models.ImageField(upload_to='selfieimages/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userID.username

class FailedAuthen(models.Model):
    FailedAuthenID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    FailedAuthenImage = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userID.username

class WebsiteList(models.Model):
    websiteListID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    websiteName = models.CharField(max_length=100, default='Website')
    websiteUrl = models.URLField()
    username = models.CharField(max_length=100, null=False)
    created_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.websiteName