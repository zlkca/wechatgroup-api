import json
import logging
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from account.models import User
from utils import to_json, create_jwt_token, decode_jwt_token

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    # def get(self, req, *args, **kwargs):
    #     try:
    #         items = User.objects.all()
    #     except Exception as e:
    #         return JsonResponse({'data':[]})
    #     return JsonResponse({'data':to_json(items)})


    def post1(self, req, *args, **kwargs):
        """ login
        """
        params = json.loads(req.body)
        item = User()
        item.username = params.get('username')
        item.first_name = params.get('first_name')
        item.last_name = params.get('last_name')
        item.portrait = params.get('portrait')
        item.type = params.get('type')
        item.save()
        return JsonResponse({'data':to_json([item])})

    def post(self, req, *args, **kwargs):
        """ login
        """
        d = json.loads(req.body)
        password = None
        r = None
        
        if d:
            password = d.get('password')
            account = d.get('account')

        if account and password:
            try:
                r = get_user_model().objects.get(Q(username__iexact=account) | Q(email__iexact=account))
            except Exception as e:  # models.DoesNotExist:
                logger.error('%s LoginView get user exception:%s'%(datetime.now(), e))
        
            if r and r.check_password(password):
                token = create_jwt_token(r.id).decode('utf-8');
                r.password = ''
                return JsonResponse({'token':token, 'data':to_json([r]) })
            else:
                return JsonResponse({'token':'', 'data':''})
        else:
            return JsonResponse({'token':'', 'data':''})

@method_decorator(csrf_exempt, name='dispatch')
class TokenView(View):
    def post(self, req, *args, **kwargs):
        """ check token
        """
        d = json.loads(req.body)
        token = None
        r = None
        
        if d:
            token = d.get('token')

        if token:
            payload = decode_jwt_token(token)

            if payload and payload.data:
                return JsonResponse({'valid':True})
            else:
                return JsonResponse({'valid':False})
        else:
            return JsonResponse({'valid':False})