from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as BaseUserManager



class Todo(models.Model):
    description = models.TextField()
    is_active = models.BooleanField(default=True)
      

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username or not password:
            raise Exception
        
        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=25, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True)


    REQUIRED_FIELDS = []
    USERNAME_FIELD = "username"

    objects = UserManager()

    def __str__(self):
        return self.username

