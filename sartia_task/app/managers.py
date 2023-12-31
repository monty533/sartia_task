from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# This is custom user model this will create the user , i have modified this because in the django by default user is save by the username.

class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        if not password:
            raise ValueError(_('Password is required'))

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        print('user',user,'',password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Super user must have is_staff true'))
        
        return self.create_user(email,password,**extra_fields)
