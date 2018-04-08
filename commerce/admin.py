from django.contrib import admin
from .models import WechatGroup, QR, Subscription

class WechatGroupAdmin(admin.ModelAdmin):
    fields = ( 'title','description', 'user', 'n_subscription','rating', 'logo')
    #readonly_fields = ('created')

admin.site.register(WechatGroup, WechatGroupAdmin)
# admin.site.register(QR)
admin.site.register(Subscription)


