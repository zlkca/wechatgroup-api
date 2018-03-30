from django.contrib import admin
from .models import WechatGroup, QR, Subscription

class WechatGroupAdmin(admin.ModelAdmin):
    fields = ( 'title','description', 'user', 'n_subscription','rating', 'image', 'image_tag', 'created')
    readonly_fields = ('n_subscription', 'rating','image_tag', 'created')

admin.site.register(WechatGroup, WechatGroupAdmin)
admin.site.register(QR)
admin.site.register(Subscription)


