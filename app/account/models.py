from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

CATEGORY = (
    ('staff', 'staff'),
    ('User', 'User')
)

EXP = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5+', '5+'),
    ('10+', '10+'),
    ('15+', '15+'),
    ('25+', '25+'),
    ('30+', '30+'),
)

MODE = (
    ('Online',  'Online'),
    ('Offline', 'Offline'),
    ('Online & Offline', 'Online & Offline'),
)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=520, blank=True, choices=CATEGORY, default='User')
    name = models.CharField(max_length=520, blank=True, null=True)
    company = models.CharField(max_length=520, blank=True, null=True)
    experience = models.CharField(
        max_length=520, blank=True, choices=EXP, default='0')
    starting_charge_price = models.FloatField(blank=True, null=True)
    mode_of_service = models.CharField(
        max_length=520, blank=True, choices=MODE, default='None')
    dob = models.DateField(blank=True, null=True)
    preferred_name = models.CharField(
        max_length=520, blank=True, null=True)
    pronoun = models.CharField(max_length=520, blank=True, null=True)
    location = models.CharField(max_length=1024, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        blank=True, null=True, upload_to='profile/%Y%m%d')
    vehicle_image=models.ImageField(blank=True, null=True, upload_to='user_vehicle_images/%Y%m%d')
    license_plate_text=models.CharField(max_length=120, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

from django.db.models.signals import post_save
from django.dispatch import receiver
from account.main import *
from app.settings import BASE_DIR

@receiver(post_save, sender=User)
def update_license_plate_text(sender, instance, **kwargs):
    try:
        if instance.vehicle_image:
            if instance.license_plate_text == None:
                img_url=instance.vehicle_image.url
                full_url =r'C:/Users/AkshayAbhi/OneDrive/Desktop/FullStackNumberPlateDetection/app'+ img_url

                texts=list()
                response = ImageToText(str(full_url))

                for template in response:
                    texts.append(template['prediction'][0]['ocr_text'])
                
                instance.license_plate_text=(", ".join(texts))
                print(f'Found texts in this image are : {texts}')   
                instance.save()
    except Exception as e:
        print(e)