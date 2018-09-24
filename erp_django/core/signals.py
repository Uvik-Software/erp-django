from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User
from guardian.shortcuts import assign_perm


@receiver(post_save, sender=User)
def do_something_when_user_updated(sender, instance, **kwargs):
    assign_perm('core.view_client', instance)


