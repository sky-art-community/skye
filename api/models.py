from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Game(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    provider_name = models.CharField(max_length=150)
    game_id = models.CharField(max_length=150)
    name = models.CharField(max_length=200)
    source_url = models.CharField(max_length=255)
    original_price = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )
    discount = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        default=0.0,
    )

    def __str__(self):
        return self.name

class Listener(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Type(models.TextChoices):
        FREE_GAME = 'FREEGAME', _('Free Game')

    type = models.CharField(
        max_length=10,
        choices=Type.choices,
    )

    class ChatType(models.TextChoices):
        USER = 'USER', _('User')
        ROOM = 'ROOM', _('Room')
        GROUP = 'GROUP', _('Group')
    
    chat_type = models.CharField(
        max_length=5,
        choices=ChatType.choices,
    )

    listener_id = models.CharField(max_length=150)
    creator_id = models.CharField(max_length=150)

    def __str__(self):
        return self.type

    """
    Save for future use perhaps
    """
 