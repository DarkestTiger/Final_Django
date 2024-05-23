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

    def get_profile_url(self):
        if self.profile_img is None:
            self.profile_img.url = static('user.png')
        else:
            return self.profile_img.url

# related_name을 following로 수정
    follower = models.ManyToManyField("self", symmetrical=False,blank=True,related_name='following')

    def __str__(self):
        return f'{self.username} 님'
    
    def get_picture(instance,filename):
        return f'user_{instance.pk}/{filename}'
    
