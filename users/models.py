from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from base.basemodel import BaseModel
from utils.cities import CITY_CHOICES as Cities


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, phone_number, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(phone_number, user_name, first_name, password, **other_fields)

    def create_user(self, phone_number, user_name, first_name, password, **other_fields):

        if not phone_number:
            raise ValueError(_('You must provide an email address'))

        user = self.model(phone_number=phone_number, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    email = models.EmailField(_('email address'), unique=True, null=True, db_index=True)
    user_name = models.CharField(_("User Name"), max_length=150, unique=True, db_index=True)
    first_name = models.CharField(_("First Name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)
    phone_number = models.CharField(_("Phone number"), max_length=15, unique=True, db_index=True)
    gender = models.CharField(_("Gender"), max_length=150, null=True, blank=True)
    age = models.CharField(_("Age"), max_length=150, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    is_active = models.BooleanField(_("Is Active"), default=True)
    photo = models.ImageField(_("Profile Photo"), upload_to='', null=True, blank=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def __str__(self):
        return self.user_name

# address model should be set on delivery apps

# class Address(BaseModel):
#     customer = models.ForeignKey(NewUser, on_delete=models.SET_NULL, null=True, related_name="customer_addresses")
#     address = models.TextField(_("Address"), max_length=250, null=True, blank=True)
#     city = models.CharField(_("City"), max_length=30, null=True, blank=True, choices=Cities)
#     district = models.CharField(_("District"), max_length=30, null=True, blank=True)
#     zip = models.CharField(_("ZIP"), max_length=30, null=True, blank=True)
#
#     def __str__(self):
#         return self.city
