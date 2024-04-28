from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, usn, name, phone_number, email, dob, gender, password=None):
        if not usn:
            raise ValueError('The USN field must be set')
        email = self.normalize_email(email)
        user = self.model(usn=usn, name=name, phone_number=phone_number, email=email, dob=dob, gender=gender)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, usn, name, phone_number, email, dob, gender, password=None):
        user = self.create_user(usn=usn, name=name, phone_number=phone_number,
                                email=email, dob=dob, gender=gender, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    usn = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')

    USERNAME_FIELD = 'usn'
    REQUIRED_FIELDS = ['name', 'phone_number', 'email', 'gender', 'dob']

    objects = UserManager()

    def __str__(self):
        return self.usn

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
