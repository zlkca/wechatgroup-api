import json
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from commerce.models import WechatGroup, Subscription

@method_decorator(csrf_exempt, name='dispatch')
class WechatGroupView(View):
   def get(self, req, *args, **kwargs):
       try:
           items = WechatGroup.objects.all()
       except Exception as e:
           return JsonResponse({'data':[]})
       d = serializers.serialize("json", items, use_natural_foreign_keys=True)
       return JsonResponse({'data':d})

   def post(self, req, *args, **kwargs):
       params = json.loads(req.body)
       item = WechatGroup()
       item.title = params.get('title')
       item.description = params.get('description')
       item.n_subscription = params.get('n_subscription')
       item.rating = params.get('rating')
       item.qr = params.get('qr')
       item.image = params.get('image')
       item.user = params.get('user')
       item.created = params.get('created')
       item.save()
       d = serializers.serialize("json", [item], use_natural_foreign_keys=True)
       return JsonResponse({'data':d})

@method_decorator(csrf_exempt, name='dispatch')
class SubscriptionView(View):
   def get(self, req, *args, **kwargs):
       try:
           items = Subscription.objects.all()
       except Exception as e:
           return JsonResponse({'data':[]})
       d = serializers.serialize("json", items, use_natural_foreign_keys=True)
       return JsonResponse({'data':d})

   def post(self, req, *args, **kwargs):
       params = json.loads(req.body)
       item = Subscription()
       item.user = params.get('user')
       item.ip = params.get('ip')
       item.wechatgroup = params.get('wechatgroup')
       item.created = params.get('created')
       item.updated = params.get('updated')
       item.save()
       d = serializers.serialize("json", [item], use_natural_foreign_keys=True)
       return JsonResponse({'data':d})

