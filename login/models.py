from locale import normalize
from django.db import models
from django.contrib.auth.models import UserManager
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser

class MainUser(AbstractUser):
    id=models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phoneno=models.BigIntegerField(unique=True,default=9087543453)
    user_loggedin=models.BooleanField(default=False)
    user_loggedout=models.BooleanField(default=False)
    user_locked=models.BooleanField(default=False)
    user_failedlogin=models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('password','phoneno')
    
    objects = CustomUserManager()

    # def _create_user(self, email, username, password, phoneno):
    #     if not email:
    #         raise ValueError('Users must have an email address')
    #     now = timezone.now()
    #     email = self.normalize_email(email)
    #     username = self.model.normalize_username(username)
    #     user = self.model(
    #         email=email,
    #         username=username, 
    #         password=password,
    #         phoneno=phoneno,
    #         date_joined=now, 
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_user(self, email, username, password, phoneno):
    #     return self._create_user(email, username, password, phoneno)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return False


    def __str__(self):
        return self.email
# Create your models here.
