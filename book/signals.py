from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import User
from .models import Rating
from .tasks import train_model_new_user, train_model_new_rating

@receiver(post_save, sender=User)
def train_model_when_new_user(sender, **kwargs):
    created = kwargs['created']
    if not created:
        return
    train_model_new_user.delay()

@receiver(post_save, sender=Rating)
def train_model_when_new_rating(sender, **kwargs):
    train_model_new_rating.delay()