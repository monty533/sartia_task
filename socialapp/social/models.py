from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import UserManager
# Create your models here.
GENDER_CHOICES=(
    ('male','Male'),
    ('female','Female')
)


class Users(AbstractBaseUser, PermissionsMixin):
    name = models.CharField( max_length=30,null=True)
    email = models.EmailField(unique=True,max_length=200)
    gender=models.CharField(choices=GENDER_CHOICES,max_length=30,null=True)
    dob = models.DateField(null=True)
    contact_no = models.BigIntegerField(null=True)
    is_available = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name

class Chats(models.Model):
    sender_id = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='sender')
    rec_id = models.ForeignKey(Users, on_delete=models.CASCADE,related_name='receiver')
    room = models.ForeignKey('ChatRoom', on_delete=models.CASCADE)
    msg = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)




    