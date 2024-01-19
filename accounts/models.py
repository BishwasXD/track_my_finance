from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password = None, confirm_password = None):

        if not email:
            raise ValueError('email not provided')

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self,email, password):
        user = self.create_user( email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length = 200, unique = True)
    is_staff = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    

    