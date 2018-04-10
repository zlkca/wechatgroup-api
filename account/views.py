import json
import logging
import base64
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login, get_user_model
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from account.models import User
from utils import to_json, create_jwt_token, decode_jwt_token

logger = logging.getLogger(__name__)

def valid_token(req):
    authorizaion = req.META['HTTP_AUTHORIZATION']
    token = authorizaion.replace("Bearer ", "")
    if token:
        s = base64.b64decode(token).decode("utf-8").replace('"', '')
        payload = decode_jwt_token(s)
        if payload and payload['data']:
            return True
    return False

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    # def get(self, req, *args, **kwargs):
    #     try:
    #         items = User.objects.all()
    #     except Exception as e:
    #         return JsonResponse({'data':[]})
    #     return JsonResponse({'data':to_json(items)})


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
                user = authenticate(req, username=r.username, password=password)
                if user is not None:
                    login(req, user) # make use of django session
                token = create_jwt_token(r.id).decode('utf-8');
                r.password = ''
                return JsonResponse({'token':token, 'data':to_json(r) })
            else:
                return JsonResponse({'token':'', 'data':''})
        else:
            return JsonResponse({'token':'', 'data':''})

@method_decorator(csrf_exempt, name='dispatch')
class TokenView(View):
    def get(self, req, *args, **kwargs):        
        if valid_token(req):
            return JsonResponse({'data':True})
        else:
            return JsonResponse({'data':False})
    
@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, req, *args, **kwargs):
        if valid_token(req):
            users = []
            try:
                users = get_user_model().objects.all()
            except Exception as e:
                logger.error('%s UserView get exception:%s'%(datetime.now(), e))
    
            return JsonResponse({'data':to_json(users)})
        else:
            return JsonResponse({'data':''})