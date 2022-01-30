from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    profile_img = models.ImageField(upload_to='profile_img', null=True, blank=True)
    status = models.CharField(max_length=150, default='Hey dear, I use connect')
    friends = models.ManyToManyField(User, blank=True, null=True, related_name='friends')
    
    skill = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.user} | {self.skill}'