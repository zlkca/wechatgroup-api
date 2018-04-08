import os
import json
import base64

from django.http import JsonResponse
from django.core import serializers
from django.core.files import File
from django.db.models import Q, Count, Max
from django.forms import ModelForm
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

from commerce.models import Category, WechatGroup, Wechat, ImageDefaultTitle, QR, Subscription
from utils import to_json, decode_jwt_token
#from unicodedata import category

User = settings.AUTH_USER_MODEL


@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(View):
    def get(self, req, *args, **kwargs):
        try:
            items = Category.objects.all()
        except Exception as e:
            return JsonResponse({'data':[]})
        return JsonResponse({'data':to_json(items)})

@method_decorator(csrf_exempt, name='dispatch')
class CategoryFormView(View):
    def get(self, req, *args, **kwargs):
        ''' get detail
        '''
        pid = int(kwargs.get('id'))
        if pid:
            try:
                item = Category.objects.get(id=pid)
            except Exception as e:
                return JsonResponse({'data':''})
        else:
            return JsonResponse({'data':''})

        return JsonResponse({'data':to_json(item)})
    
    def delete(self, req, *args, **kwargs):
        pid = int(kwargs.get('id'))
        if pid:
            instance = Category.objects.get(id=pid)
            instance.delete()
            items = Category.objects.filter().order_by('-id')
            return JsonResponse({'data':to_json(items)})
        return JsonResponse({'data':[]})
    
    def post(self, req, *args, **kwargs):
        params = json.loads(req.body)

        _id = params.get('id')
        if _id:
            item = Category.objects.get(id=_id)
        else:                    
            item = Category()
            
        item.name = params.get('name')
        item.description = params.get('description')
        item.status = params.get('status')
        item.save()
        return JsonResponse({'data':to_json(item)})

@method_decorator(csrf_exempt, name='dispatch')
class WechatGroupListView(View):
    
    def get(self, req, *args, **kwargs):
        keyword = req.GET.get('keyword')
        category_id = req.GET.get('category_id')
        
        try:
            if keyword:
                items = WechatGroup.objects.filter(Q(title__icontains=keyword)|Q(description__icontains=keyword)|Q(category__name__icontains=keyword)).order_by('-id')
            elif category_id:
                items = WechatGroup.objects.filter(category_id=category_id).order_by('-id')
            else:
                items = WechatGroup.objects.filter().order_by('-id')
        except Exception as e:
            return JsonResponse({'data':[]})
        #d = serializers.serialize("json", items, use_natural_foreign_keys=True)
        return JsonResponse({'data':to_json(items)})
        
    

@method_decorator(csrf_exempt, name='dispatch')
class WechatGroupFormView(View):        
    def get(self, req, *args, **kwargs):
        ''' get detail
        '''
        pid = int(kwargs.get('id'))
        if pid:
            try:
                item = WechatGroup.objects.select_related('category').get(id=pid)
            except Exception as e:
                return JsonResponse({'data':''})
        else:
            return JsonResponse({'data':''})
        
        qrs = QR.objects.filter(wechatgroup_id=item.id)
        wechatgroup = to_json(item)
        wechatgroup['qrs'] = to_json(qrs)
        return JsonResponse({'data':wechatgroup})
    
    def delete(self, req, *args, **kwargs):
        pid = int(kwargs.get('id'))
        if pid:
            instance = WechatGroup.objects.get(id=pid)
            instance.delete()
            items = WechatGroup.objects.filter().order_by('-id')
            return JsonResponse({'data':to_json(items)})
        return JsonResponse({'data':[]})
    
    def post(self, req, *args, **kwargs):
        ''' create item
        '''
        params = req.POST
        authorizaion = req.META['HTTP_AUTHORIZATION']
        token = authorizaion.replace("Bearer ", "")
        if token:
            payload = decode_jwt_token(base64.b64decode(token))
            if payload and payload['data']:
                try:
                    user = get_user_model().objects.get(id=req.POST.get('user_id'))
                except:
                    user = None
                try:
                    category = Category.objects.get(id=req.POST.get('category_id'))
                except:
                    category = None
                    
                _id = params.get('id')
                qrs = None
                if _id:
                    item = WechatGroup.objects.get(id=_id)
                else:                    
                    item = WechatGroup()

                item.title = params.get('title')
                item.description = params.get('description')
                item.n_subscription = params.get('n_subscription')
                item.rating = params.get('rating')
                item.user = user
                item.category = category

                item.save()

                if _id:
                    qrs = QR.objects.filter(wechatgroup_id=_id)
                    for qr in qrs:
                        self.saveQR(qr, req, params, item)
                else:
                    for i in range(4):
                        qr = QR()
                        qr.index = i
                        self.saveQR(qr, req, params, item)

                
                qrs = QR.objects.filter(wechatgroup_id=item.id)
                item.logo = self.getDefaultLogo(qrs)
                item.save()

                wechatgroup = to_json(item)
                wechatgroup['qrs'] = to_json(qrs)
                #d = serializers.serialize("json", [item], use_natural_foreign_keys=True)
                return JsonResponse({'tokenValid': True,'data':to_json(item)})
        return JsonResponse({'tokenValid':False, 'data':''})
    

    def getDefaultLogo(self, qrs):
        if qrs[0].image.name:
            return qrs[0].image.name
        elif qrs[1].image.name:
            return qrs[1].image.name;
        elif qrs[2].image.name:
            return qrs[2].image.name;
        elif qrs[3].image.name:
            return qrs[3].image.name;
        else:
            return ''


    def saveQR(self, qr, req, params, wechatgroup):
        i = qr.index
        qr.title = params.get('title%s'%i)
        image = req.FILES.get('image%s'%i)
        qr.wechatgroup = wechatgroup
        if image:
            qr.image.save(image.name, image.file, True)
        else:
            if params.get('image_status%s'%i) == 'clear':
                try:
                    os.remove(qr.image.path)
                except:
                    print('remove image failed')
                qr.image.delete()
            
        qr.save()

@method_decorator(csrf_exempt, name='dispatch')
class WechatFormView(View):        
    def get(self, req, *args, **kwargs):
        ''' get detail
        '''
        pid = int(kwargs.get('id'))
        if pid:
            try:
                item = Wechat.objects.get(id=pid)
            except Exception as e:
                return JsonResponse({'data':''})
        else:
            return JsonResponse({'data':''})

        return JsonResponse({'data':to_json(item)})
    
    def delete(self, req, *args, **kwargs):
        pid = int(kwargs.get('id'))
        if pid:
            instance = Wechat.objects.get(id=pid)
            instance.delete()
            items = Wechat.objects.filter().order_by('-id')
            return JsonResponse({'data':to_json(items)})
        return JsonResponse({'data':[]})
    
    def post(self, req, *args, **kwargs):
        ''' create item
        '''
        params = req.POST
        authorizaion = req.META['HTTP_AUTHORIZATION']
        token = authorizaion.replace("Bearer ", "")
        if token:
            payload = decode_jwt_token(base64.b64decode(token))
            if payload and payload['data']:
                    
                _id = params.get('id')
                if _id:
                    item = Wechat.objects.get(id=_id)
                else:                    
                    item = Wechat()
                    
                item.title = params.get('title')
                item.description = params.get('description')
                logo = req.FILES.get('logo')
                if logo:
                    item.logo.save(logo.name, logo.file, True)
                item.save()
                
                #d = serializers.serialize("json", [item], use_natural_foreign_keys=True)
                return JsonResponse({'tokenValid': True,'data':to_json(item)})
        return JsonResponse({'tokenValid':False, 'data':''})

@method_decorator(csrf_exempt, name='dispatch')
class ImageDefaultTitleFormView(View):        
    def get(self, req, *args, **kwargs):
        ''' get detail
        '''
        pid = int(kwargs.get('id'))
        if pid:
            try:
                item = ImageDefaultTitle.objects.get(id=pid)
            except Exception as e:
                return JsonResponse({'data':''})
        else:
            return JsonResponse({'data':''})

        return JsonResponse({'data':to_json(item)})
    
    def post(self, req, *args, **kwargs):
        ''' create item
        '''
        params = req.body.decode('utf8').replace("'", '"')#req.POST
        params = json.loads(params)
        authorizaion = req.META['HTTP_AUTHORIZATION']
        token = authorizaion.replace("Bearer ", "")
        if token:
            payload = decode_jwt_token(base64.b64decode(token))
            if payload and payload['data']:                    
                _id = params.get('id')
                if _id:
                    item = ImageDefaultTitle.objects.get(id=_id)
                else:                    
                    item = ImageDefaultTitle()
                    
                item.name0 = params.get('name0')
                item.name1 = params.get('name1')
                item.name2 = params.get('name2')
                item.name3 = params.get('name3')
                
                item.save()
                
                #d = serializers.serialize("json", [item], use_natural_foreign_keys=True)
                return JsonResponse({'tokenValid': True,'data':to_json(item)})
        return JsonResponse({'tokenValid':False, 'data':''})
 
        
@method_decorator(csrf_exempt, name='dispatch')
class QRFormView(View):
   def get(self, req, *args, **kwargs):
       try:
           items = QR.objects.all()
       except Exception as e:
           return JsonResponse({'data':[]})
       return JsonResponse({'data':to_json(items)})

   def post(self, req, *args, **kwargs):
       params = json.loads(req.body)
       item = QR()
       item.title = params.get('title')
       item.image = params.get('image')
       wechatgroup_id = params.get('wechatgroup_id')
       try:
           item.wechatgroup = WechatGroup.objects.get(id=wechatgroup_id)
       except:
           item.wechatgroup = None
       item.save()
       return JsonResponse({'data':to_json(item)})
                        
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

