from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError

class RegistrationForm(UserCreationForm):
    first_name=forms.CharField(max_length=40,required=True,widget=forms.TextInput(attrs={'class':'form-control','style':'width:50%'}))
    last_name=forms.CharField(max_length=40,required=True,widget=forms.TextInput(attrs={'class':'form-control','style':'width:50%'}))
    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class':'form-control','style':'width:50%'}))
    username=forms.CharField(max_length=40,required=True,widget=forms.TextInput(attrs={'class':'form-control','id':'custom-width','style':'width:50%'}))
    password1=forms.CharField(max_length=40,required=True,widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:50%'}))
    password2=forms.CharField(max_length=40,required=True,widget=forms.PasswordInput(attrs={'class':'form-control','style':'width:50%'}))
    class Meta:
        model=User
        fields = ['first_name','last_name', 'username','email', 'password1', 'password2']

def clean_email(self):
    email=self.cleaned_data['email']
    User=None
    try:
        User.objects.get(email=email)
    except :
        return email     

    if(User is not None):
        raise ValidationError("already exists")
