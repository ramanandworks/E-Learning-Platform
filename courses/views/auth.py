from django.http import HttpResponse
from django.shortcuts import render,redirect
from courses.models import Course, Video
from courses import models
from django.contrib.auth.forms import UserCreationForm
from courses.forms import RegistrationForm,LoginForm
from django.views import View
from django.contrib.auth import logout


class signupview(View):
    def get(self,request):
        form=RegistrationForm()
        return render(request,template_name='courses/signup.html',context={'form':form})
    

    def post(self,request):
        form=RegistrationForm(request.POST)
        if (form.is_valid()):
            user=form.save()
            if(user is not None):
                return redirect('login')
        # print(user.first_name,user.email)
        return render(request,template_name='courses/signup.html',context={'form':form})

# def signup(request):
#     if(request.method=="GET"):
#         form=RegistrationForm()
#         return render(request,template_name='courses/signup.html',context={'form':form})
    
#     form=RegistrationForm(request.POST)
#     if (form.is_valid()):
#         user=form.save()
#         if(user is not None):
#             return redirect('login')
#         print(user.first_name,user.email)
#     return render(request,template_name='courses/signup.html',context={'form':form})
    


class loginview(View):
    def get(self,request):
        form=LoginForm()
        context={
        'form':form
        }
        return render(request,template_name='courses/login.html',context=context)


    def post(self,request):
        form=LoginForm(request=request,data=request.POST)
        context={
            'form':form
        }
        if(form.is_valid()):
            return redirect('home')     
        return render(request,template_name='courses/login.html',context=context)
    

def signout(request):
    logout(request)
    return redirect('home')