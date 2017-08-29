from django import forms
from django.contrib.auth.models import User
from .models import ProfileUser

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    password=forms.CharField(label='请输入密码',widget=forms.PasswordInput)
    password2=forms.CharField(label='请再次输入密码',widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','email')

    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('两次密码不一致')
        return cd['password2']
class EmailForm(forms.Form):
    email=forms.EmailField()

class PasswordForm(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('first_name','last_name')

class ProfileUserEditForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ('birth','come_from','photo','others')
        widgets = {'birth':forms.SelectDateWidget(years=range(1900,2020))}
