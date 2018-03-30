from django.contrib import admin
from .models import WechatGroup, Subscription

class WechatGroupAdmin(admin.ModelAdmin):
    fields = ( 'image', 'image_tag')
    readonly_fields = ('image_tag',)

admin.site.register(WechatGroup, WechatGroupAdmin)
admin.site.register(Subscription)

