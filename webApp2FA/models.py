from django.db import models
from django.contrib.auth.models import User

class UserImage(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    userImage = models.ImageField(upload_to='selfieimages/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userID.username
    
class IntruderImage(models.Model):
    IntruderImageID = models.AutoField(primary_key=True)
    userID = models.OneToOneField(User, on_delete=models.CASCADE)
    intruderImage = models.ImageField(upload_to='intruderimages/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.userID.username
    
class WebsiteList(models.Model):
    websiteListID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    websiteName = models.CharField(max_length=100, default='Website')
    websiteUrl = models.URLField()
    created_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.websiteName