from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static

LOCAL_HOST="http://127.0.0.1:8000/"

# 유저모델
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(upload_to="profile/images/", blank=True)
    address = models.CharField(max_length=300)
    introduce = models.TextField(blank=True)

    follower = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='following')
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def get_profile_url(self):
        if not self.profile_img:
            return static('user.png')
        return self.profile_img.url

    def __str__(self):
        return f'{self.username} 님'
    
    def get_picture(instance,filename):
        return f'user_{instance.pk}/{filename}'
    
