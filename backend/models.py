from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class StudentManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The PRN (username) must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(username, password, **extra_fields)


class Student(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)  
    name = models.TextField()  
    class_name = models.CharField(max_length=50) 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Candidate(models.Model):
    name = models.CharField(max_length=100)
    prn = models.CharField(max_length=20, unique=True) 
    class_name = models.CharField(max_length=50)  
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.class_name})"
