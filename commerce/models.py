import uuid
import os

from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
#from django.conf.settings import AUTH_USER_MODEL as User
from django.db.models import CharField, Model, ForeignKey, DateTimeField, DecimalField, IntegerField, ImageField, BooleanField

#from accounts.models import Address
# from itertools import count
# from crypto import Crypto
# from pycparser.ply.yacc import token

CATERGORIES = (('furniture','Furniture'), ('cad', 'CAD'))
CURRENCIES = (('usd','USD'), ('cad', 'CAD'), ('cny','CNY'))
STATUS = (('active','Active'), ('inactive', 'Inactive'))
PROFESSIONS = (('FA','Financial advisor'), ('MB', 'Mortgage Broker'), ('AC','Accountant'))

User = settings.AUTH_USER_MODEL

class Category(Model):
    name = CharField(max_length=64, null=True, blank=True)
    description = CharField(max_length=500, null=True, blank=True)
    status = CharField(max_length=16, choices=STATUS, default='active')

    def __str__(self):
        return self.name

def get_upload_logo_path(instance, fname):
    user_id = '0'
    _id = '0'
    if instance.id:
        _id = instance.id
        if instance.user:
            user_id = instance.user.id
    return os.path.join('logo', str(user_id), str(_id), fname)

class WechatGroup(Model):
    title = CharField(max_length=128, null=True, blank = True)
    description = CharField(max_length=800, null=True, blank = True)
    n_subscription = DecimalField(max_digits=10, decimal_places=3, null=True)
    rating = DecimalField(max_digits=10, decimal_places=3, null=True)
    #logo = CharField(max_length=256, null=True, blank = True)
    logo = ImageField(upload_to=get_upload_logo_path)
    category = ForeignKey(Category, null=True, blank=True, db_column='category_id', on_delete=models.CASCADE)
    user = ForeignKey(User, null=True, blank=True, db_column='user_id', on_delete=models.CASCADE)
    created = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_logo_path(self, fname):
        user_id = '0'
        product_id = '0'
        title = self.title
        if self.user:
            user_id = self.user.id

        return os.path.join('logo', str(user_id), str(title), fname)

    # def image_tag(self):
    #     return mark_safe('<img style="width:100px;" src="%s" />' % self.logo.url)

    # image_tag.short_description = 'Image'
    # image_tag.allow_tags = True

def get_upload_qr_path(instance, fname):
    author_id = '0'
    _id = '0'
    if instance.wechatgroup:
        _id = instance.wechatgroup.id
        if instance.wechatgroup.user:
            user_id = instance.wechatgroup.user.id
    return os.path.join('qr', str(user_id), str(_id), fname)

class QR(Model):
    title = CharField(max_length=128, null=True, blank=True)
    image = ImageField(upload_to=get_upload_qr_path)
    wechatgroup = ForeignKey(WechatGroup, null=True, blank=True, db_column='wechatgroup_id', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def image_tag(self):
        return '<img src="%s" />' % self.image.url

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "url": self.image.url,
            "width": self.image.width,
            "height": self.image.height,
            "wechatgroup_id": self.wechatgroup.id
        }

class Subscription(Model):
    user = ForeignKey(User, null=True, blank=True, db_column='user_id', on_delete=models.CASCADE)
    ip = CharField(max_length=64, null=True, blank=True)
    wechatgroup = ForeignKey(WechatGroup, null=True, blank=True, on_delete=models.CASCADE)
    status = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username if self.user else self.ip

# class Comment(Model):
#     body = CharField(max_length=800, null=True, blank=True)
#     wechatgroup = ForeignKey(WechatGroup, null=True, blank=True, db_column='wechatgroup_id', on_delete=models.CASCADE)
#     user = ForeignKey(User, null=True, blank=True, db_column='user_id', on_delete=models.CASCADE)
#     created = DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.body

