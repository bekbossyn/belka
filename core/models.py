# -*- coding: utf-8 -*-
import json
import random
from datetime import timedelta
import requests

from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import GameSetting
from . import tasks
from utils.constants import HIDE_LAST, LANGUAGES, RUSSIAN
from utils.image_utils import get_url

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.core.files import File
from django.db import models
from django.template.loader import render_to_string

from io import BytesIO
# from utils import mobizonproxy
from utils.messages import REGISTRATION_COMPLETE, PASSWORD_EMAIL_RESET
from utils.upload import avatar_upload, avatar_upload_v2, get_random_name


class MainUserManager(BaseUserManager):
    """
    Custom user manager.
    """

    def create_user(self, phone, password):
        """
        Creates and saves a User with the given phone and password
        """
        if not phone or not password:
            raise ValueError('Users must have an phone and password')

        user = self.model(phone=phone.lower())
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password):
        """
        Creates and saves a superuser with the given phone and password
        """
        user = self.create_user(phone=phone,
                                password=password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MainUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with phone .
    """
    phone = models.CharField(max_length=200, blank=True, null=True, unique=True, db_index=True)
    name = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True, null=True, unique=True, db_index=True)
    # fb_id = models.CharField(max_length=200, blank=True, null=True, unique=True, db_index=True)
    # insta_id = models.CharField(max_length=200, blank=True, null=True, unique=True, db_index=True)
    # vk_id = models.CharField(max_length=200, blank=True, null=True, unique=True, db_index=True)
    # languages = models.ManyToManyField('Language')
    language = models.IntegerField(choices=LANGUAGES, default=RUSSIAN)

    avatar = models.ImageField(upload_to=avatar_upload, blank=True, null=True)
    avatar_big = models.ImageField(upload_to=avatar_upload, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    review = models.FloatField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    #   for one signal notifications
    player_ids = ArrayField(models.CharField(max_length=255, blank=True, null=True, default=""), default=list)

    objects = MainUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.phone

    def __unicode__(self):
        return self.phone

    def __str__(self):
        return self.phone or self.email
        # or self.vk_id or self.fb_id or self.insta_id

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin

    def json(self, short=False, user=None):
        if not short:
            result = {
                "user_id": self.pk,
                "phone": self.hidden_phone(user),
                "name": self.name,
                "email": self.hidden_email(user),
                "avatar": get_url(self.avatar),
                "avatar_big": get_url(self.avatar_big) or get_url(self.avatar),
                # "languages": [l.name for l in self.languages.all()],
                "language_id": self.language,
                "language": self.get_language_display(),
                "review": self.review if self.review else None,
                # "reviews": [r.json(user) for r in self.reviews.all()],
                "verified": self.verified(),
                'game_setting': self.game_setting.json(),
            }
        else:
            result = {
                "user_id": self.pk,
                "phone": self.hidden_phone(user),
                "email": self.hidden_email(user),
                "name": self.name,
                "avatar": get_url(self.avatar),
            }
        return result

    def owner_json(self, short=False):
        if not short:
            result = {
                "user_id": self.pk,
                "phone": self.phone,
                "name": self.name,
                "email": self.email,
                "avatar": get_url(self.avatar),
                "avatar_big": get_url(self.avatar_big) or get_url(self.avatar),
                # "languages": [l.name for l in self.languages.all()],
                "language_id": self.language,
                "language": self.get_language_display(),
                "review": self.review if self.review else None,
                # "reviews": [r.json(user=self) for r in self.reviews.all()],
                "verified": self.verified(),
                'game_setting': self.game_setting.json(),
            }
        else:
            result = {
                "user_id": self.pk,
                "phone": self.phone,
                "email": self.email,
                "name": self.name,
                "avatar": get_url(self.avatar),
            }
        return result

    def hidden_email(self, user=None):
        if self.email and user != self:
            return '*' * len(self.email)
        return self.email or None

    def hidden_phone(self, user=None):
        if self.phone and user != self:
            return self.phone[:(len(self.phone) - HIDE_LAST)] + '*' * HIDE_LAST
        return self.phone or None

    def verified(self):
        email = False
        if self.email:
            email = True

        phone = False
        if self.phone:
            phone = True

        return {
            "phone": phone,
            "email": email,
        }

    # def set_social_id(self, social_type, social_id):
    #     if social_type == "facebook" and not self.fb_id:
    #         self.fb_id = social_id
    #         self.save()
    #     elif social_type == "vk" and not self.vk_id:
    #         self.vk_id = social_id
    #         self.save()
    #     elif social_type == "insta" and not self.insta_id:
    #         self.insta_id = social_id
    #         self.save()
    #     elif social_type == "google" and not self.email:
    #         self.email = social_id
    #         self.save()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    # def save(self, *args, **kwargs):
    #     if self.contact_number is None and self.phone:
    #         self.contact_number = self.phone
    #     super(MainUser, self).save(*args, **kwargs)


@receiver(post_save, sender=MainUser)
def create_game_settings(sender, instance, **kwargs):
    """
        Create game_settings for the user, if does not exist
    """
    _ = GameSetting.objects.get_or_create(owner=instance)


class TokenLog(models.Model):
    """
    Token log model
    """
    token = models.CharField(max_length=500, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tokens', null=False, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return u"Token {0} of user {1}".format(self.pk, self.user_id)

    class Meta:
        index_together = [
            ["token", "user"]
        ]


class ActivationManager(models.Manager):
    """
    Custom manager for Activation model
    """

    def create_social_code(self, email, phone, password):
        """
        Creates activation code and sends SMS via mobizon.kz service.
        Stores hashed password.
        TODO: Logging
        """
        # code = "4512"
        code = "1111"
        activation = Activation(phone=phone,
                                email=email,
                                to_reset=False,
                                password=make_password(password),
                                code=code)
        activation.save()
        return activation

    def create_email_code(self, email, password):
        """
        Creates activation code and sends SMS via mobizon.kz service.
        Stores hashed password.
        TODO: Logging
        """
        # code = "%0.4d" % random.randint(0, 9999)
        code = "1111"
        activation = Activation(email=email,
                                to_reset=False,
                                password=make_password(password),
                                code=code)
        activation.save()
        return activation

    def create_email_reset_code(self, email, new_password):
        code = "1111"
        activation = Activation(email=email,
                                to_reset=True,
                                to_change_phone=False,
                                to_change_email=False,
                                password=make_password(new_password),
                                code=code)
        activation.save()
        return activation

    def create_code(self, phone, password):
        """
        Creates activation code and sends SMS via mobizon.kz service.
        Stores hashed password.
        TODO: Logging
        """
        code = "1111"

        # if phone in ["+77753721232", "+77752470125", "+77074443333", "+77076799939"]:
        #     code = "4512"
        # else:
        #     code = "%0.4d" % random.randint(0, 9999)

        # mobizonproxy.send_sms(phone, text=u"{} - Код активации для Pillowz365".format(code))
        activation = Activation(phone=phone,
                                to_reset=False,
                                password=make_password(password),
                                code=code)
        activation.save()
        return activation

    def create_code_without_password(self, phone):
        """
        Creates activation code and sends SMS via mobizon.kz service.
        Stores hashed password.
        TODO: Logging
        """

        code = "1111"

        # if phone in ["+77753721232", "+77752470125", "+77074443333"]:
        #     code = "4512"
        # else:
        #     code = "%0.4d" % random.randint(0, 9999)
        #     mobizonproxy.send_sms(phone, text=u"{} - Код активации для Pillowz365".format(code))
        activation = Activation(phone=phone,
                                to_reset=False,
                                password=make_password(code),
                                code=code)
        activation.save()
        return activation

    def create_phone_change_code(self, phone, email, new_phone):
        """
        Creates activation code and sends SMS via mobizon.kz service.
        Stores hashed password.
        TODO: Logging
        """

        code = "1111"

        # if new_phone in ["+77753721232", "+77752470125", "+77074443333"]:
        #     code = "4512"
        # else:
        #     code = "%0.4d" % random.randint(0, 9999)
        #     mobizonproxy.send_sms(new_phone, text=u"{} - Код подтверждения для Pillowz365".format(code))
        activation = Activation(phone=phone,
                                email=email,
                                new_phone=new_phone,
                                to_reset=False,
                                to_change_phone=True,
                                to_change_email=False,
                                password=make_password(code),
                                code=code)
        activation.save()
        return activation

    def create_email_change_code(self, email, phone, new_email):
        """
        Creates activation code and sends SMS via mobizon.kz service.
        Stores hashed password.
        TODO: Logging
        """

        code = "1111"

        # if new_phone in ["+77753721232", "+77752470125", "+77074443333"]:
        #     code = "4512"
        # else:
        #     code = "%0.4d" % random.randint(0, 9999)
        #     mobizonproxy.send_sms(new_email, text=u"{} - Код подтверждения для Pillowz365".format(code))
        activation = Activation(email=email,
                                phone=phone,
                                new_email=new_email,
                                to_reset=False,
                                to_change_email=True,
                                to_change_phone=False,
                                password=make_password(code),
                                code=code)
        activation.save()
        return activation

    def create_reset_code(self, phone, new_password):
        """
        Creates activation code and sends SMS via mobizon.kz service.
        Stores hashed password.
        TODO: Logging
        """

        code = "1111"

        # if phone in ["+77753721232", "+77752470125", "+77074443333"]:
        #     code = "4512"
        # else:
        #     code = "%0.4d" % random.randint(0, 9999)
        #     mobizonproxy.send_sms(phone, text=u"{} - Код активации для Pillowz365".format(code))
        activation = Activation(phone=phone,
                                to_reset=True,
                                password=make_password(new_password),
                                code=code)
        activation.save()
        return activation


class Activation(models.Model):
    """
    Stores information about activations
    """
    name = models.CharField(max_length=255, blank=True, null=True)

    phone = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    new_phone = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    email = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    new_email = models.CharField(max_length=100, blank=True, null=True, db_index=True)

    password = models.CharField(max_length=100, blank=False, db_index=True)
    code = models.CharField(max_length=100, blank=False, db_index=True)
    used = models.BooleanField(default=False, db_index=True)

    to_reset = models.BooleanField(default=False, db_index=True)
    to_change_phone = models.BooleanField(default=False, db_index=True)
    to_change_email = models.BooleanField(default=False, db_index=True)

    objects = ActivationManager()

    # fb_id = models.CharField(max_length=200, blank=True, null=True)
    # insta_id = models.CharField(max_length=200, blank=True, null=True)
    # vk_id = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to=avatar_upload_v2, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def send_email(self):
        message = render_to_string('emails/activation.html',
                                   context={'code': self.code})
        tasks.email(to=self.email, subject=REGISTRATION_COMPLETE["ru"], message=message)

    def send_reset_email(self):
        message = render_to_string('emails/activation.html',
                                   context={'code': self.code,
                                            'reset': True})
        tasks.email(to=self.email, subject=PASSWORD_EMAIL_RESET["ru"], message=message)

    def send_sms(self):
        self.code = "1111"
        # if self.phone in ["+77753721232", "+77752470125", "+77074443333", "+77076799939"]:
        #     self.code = "4512"
        # mobizonproxy.send_sms(self.phone, text=u"{} - Код активации для Pillowz365".format(self.code))

    def __unicode__(self):
        return u"{0} {1}".format(self.phone, self.code)

    # def set_social_id(self, social_type, social_id):
    #     if social_type == "facebook" and not self.fb_id:
    #         self.fb_id = social_id
    #     elif social_type == "vk" and not self.vk_id:
    #         self.vk_id = social_id
    #     elif social_type == "insta" and not self.insta_id:
    #         self.insta_id = social_id
    #     elif social_type == "google" and not self.email:
    #         self.email = social_id

    def handle_avatar(self, url, save=True):
        """
        Downloads image from url & saves to local storage
        """
        response = requests.get(url)
        if response.status_code == 200:
            fp = BytesIO(response.content)
            ext = url.split('.')[-1]
            ext = ext if ext in ["png", "jpg", "gif", "jpeg"] else "jpg"
            filename = "{}.{}".format(get_random_name(), ext)
            self.avatar.save(filename, File(fp), save=save)

    class Meta:
        ordering = ['-timestamp']
        index_together = [
            ["phone", "email", "used"]
        ]


