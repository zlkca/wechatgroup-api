from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.db.models import CharField, Model, ForeignKey, DateTimeField, DecimalField, IntegerField, ImageField

USER_TYPES = (('member','Member'), ('merchant', 'Merchant'))

class User(AbstractUser):
    """ type --- 'guest', 'member', 'admin'
    """
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    portrait = CharField(max_length=256, null=True, blank=True) # main, google, facebook, wechat, qq, taobao
    type = CharField(max_length=16, choices=USER_TYPES, default='member')

    def natural_key(self):
        return (self.id, self.username)
