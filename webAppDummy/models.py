from django.db import models

class DummyUser(models.Model):
    DummyUserID = models.AutoField(primary_key=True)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.Email