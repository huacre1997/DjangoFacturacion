from django.shortcuts import render
from django.template.loader import render_to_string

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import json
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import User
from django.http import HttpResponse
from .forms import UserForm
class UserListView(generic.ListView,LoginRequiredMixin):
    model=User
    template_name="user/UserList.html"
    login_url = "bases:login"
    @method_decorator(csrf_exempt)
    def dispatch(self,request,*args, **kwargs):
        return super().dispatch(request,*args,**kwargs)
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="searchData":
                data=[]
                for i in User.objects.all():
                    data.append(i.toJSON())
               
            else:
                data["error"]="Ha ocurrido un error"
        except Exception as e:
            print(e)
        return JsonResponse(data,safe=False)
class CreateUserView(generic.CreateView,LoginRequiredMixin):
    model = User
    form_class = UserForm
    login_url = "bases:login"
    template_name="user/user_form.html"
    def post(self,request,*args, **kwargs):
        data={}
        try:
            action=request.POST["action"]
            if action=="add":
                form = self.get_form()
                print(form)
                if form.is_valid():
                   
                    form.save()
                    data = {
                    'stat': 'ok',
                    'form': render_to_string(self.template_name, {'form': form}, request=request)}
                    return JsonResponse(data)

                else:
                    data = render_to_string(self.template_name,{'form': form}, request=request)
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data["error"]="Nose ha ingresado nada s"
        except Exception as e:
            print(e)
       