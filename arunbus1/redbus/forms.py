from django import forms
from django.contrib.auth import(
         authenticate,
         get_user_model
)

User=get_user_model()

class UserLoginForm(forms.Form):
         username=forms.CharField()
         password=forms.CharField(widget=forms.PasswordInput)

         def clean(self,*args,**kwargs):
                  username=self.cleaned_data.get('username')
                  password=self.cleaned_data.get('password')
                  if username and password:
                           user=authenticate(username=username, password=password)
                           if not user:
                                    raise forms.ValidationError('user does not exist')
                           if not user.check_password(password):
                                    raise forms.ValidationError('invalid password')
                           if not user.is_active:
                                    raise forms.ValidationError('User is not active')
                           return super(UserLoginForm,self).clean(*args,**kwargs)
class UserRegisterForm(forms.ModelForm):
         email=forms.EmailField(label='Email address')
         password=forms.CharField(widget=forms.PasswordInput)
         class Meta:
                  fields=[
                           'username',
                           'email',
                           'password'
                           ]
         def clean(self,*args,**kwargs):
                  username=self.cleaned_data.get('email')
                  email_qs=User.objects.filter(email=email)
                  if email_qs.exists():
                           raise forms.ValidationError(
                                    "email already exist")
                  return super(UserLoginForm,self).clean(*args,**kwargs)
                  

                  
         
