from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
# Create your models here.

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user=instance)
>>>>>>> 93ab2cef756ccefa791414084b892022eced804e
