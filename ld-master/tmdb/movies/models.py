from django.db import models
from django.shortcuts import redirect, reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

from django.contrib.auth.models import User

from rest_framework.reverse import reverse as api_reverse


# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    slug = models.SlugField(blank=True, null=True)
    mail = models.CharField(max_length=1000)

def unique_slug_generator_user(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.user.username)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator_user(instance, new_slug=new_slug)
    return slug


        
def profile_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_user(instance)
pre_save.connect(profile_pre_save_receiver, sender=UserProfile)

def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created == True:
        UserProfile.objects.create(user=instance)
        u1 = UserProfile.objects.get(user=instance)
        u1.title = instance.username
post_save.connect(user_post_save_receiver, sender=User)