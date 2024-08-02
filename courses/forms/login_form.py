from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate,login


class LoginForm(AuthenticationForm):
    username=forms.CharField(max_length=50,required=True,widget=forms.TextInput(attrs={'class':'form-control','style':'width:50%'}))
    password=forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:50%'}))
    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        user=None
        try:
            user=User.objects.get(username=username)
            result=authenticate(username=user.username,password=password)
            print("result",result)
            if(result is not None):
                login(self.request,result)
                return result
            else:
                raise ValidationError("Invalid username or password")

        except:
            raise ValidationError("Invalid username or password")

    
