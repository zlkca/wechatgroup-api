import json
from django.http import JsonResponse
from django.core import serializers
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from account.models import User

@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
   def get(self, req, *args, **kwargs):
       try:
           items = User.objects.all()
       except Exception as e:
           return JsonResponse({'data':[]})
       d = serializers.serialize("json", items, use_natural_foreign_keys=True)
       return JsonResponse({'data':d})

   def post(self, req, *args, **kwargs):
       params = json.loads(req.body)
       item = User()
       item.username = models.CharField( = params.get('username = models.CharField(')
       item.first_name = models.CharField(_('first name'), max_length=30, blank=True) = params.get('first_name = models.CharField(_('first name'), max_length=30, blank=True)')
       item.last_name = models.CharField(_('last name'), max_length=150, blank=True) = params.get('last_name = models.CharField(_('last name'), max_length=150, blank=True)')
       item.portrait = params.get('portrait')
       item.type = params.get('type')
       item.save()
       d = serializers.serialize("json", [item], use_natural_foreign_keys=True)
       return JsonResponse({'data':d})

