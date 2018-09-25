from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=User)
def do_something_when_user_updated(sender, instance, created, update_fields, **kwargs):

    def disconnect_signal(signal, receiver, sender):
        disconnect = getattr(signal, 'disconnect')
        disconnect(receiver, sender)

    def reconnect_signal(signal, receiver, sender):
        connect = getattr(signal, 'connect')
        connect(receiver, sender=sender)
