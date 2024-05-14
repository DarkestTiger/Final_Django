from django.db import models
from django.contrib.auth.models import AbstractUser


# 유저모델
class User(AbstractUser):
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True)
    profile_img = models.ImageField(upload_to="media/profile") # media 스펠링 수정, pillow 설치
    introduce = models.TextField(max_length=300) # models, max_length 수정
    follower = models.ManyToManyField("self", symmetrical=False,blank=True,related_name='followers')

    def __str__(self):
        return f'{self.username} 님'
    
    def get_picture(instance,filename):
        return f'user_{instance.pk}/{filename}'