from django.shortcuts import render,HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.core.mail import send_mail
from django.contrib import messages
from .forms import LoginForm,RegisterForm,EmailForm,PasswordForm,UserEditForm,ProfileUserEditForm
from .models import ProfileUser
import random
import uuid
import base64
# Create your views here.

def email_confirm(email,type):
    if type=='yzm':
        ran=random.randint(100000,999999)
        subject='来自ttwilight.cn的注册邮件'
        body="[ttwilight]你的邮箱注册验证码是"+str(ran)+",千万不要告诉别人。"
        send_mail(subject,body,'1063255195@qq.com',[email],fail_silently=False)
        return ran
    elif type=='reset':
        per_str=email+'reset'
        per_id=uuid.uuid3(uuid.NAMESPACE_DNS,per_str)
        per_m=base64.b64encode(email.encode('utf-8'))
        subject='来自ttwilight.cn的密码找回邮件'
        link='http://127.0.0.1:8000/account/password_reset/confirm/'+per_m.decode('utf-8')+'/'+str(per_id)
        body="[ttwilight]您正在尝试找回密码，如果确认是本人操作，请将下面链接复制到浏览器地址栏打开：<a href=%s>%s</a>" % (link,link)
        send_mail(subject,body,'1063255195@qq.com',[email],fail_silently=False,html_message=body)   #html_message 发送html格式邮件

def check_login(request):
    if request.user.username!='':
        return True
    return False

def account_page(request):
    if check_login(request):
        user=request.user
        return render(request,'account/welcome.html',{'user':user})
    return HttpResponseRedirect('login')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/account/login')

def user_login(request):
    if request.method=='POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            cd=login_form.cleaned_data
            user=authenticate(username=cd['username'],password=cd['password'])
            if user:
                if user.is_active:
                    login(request,user)
                    return render(request,'account/welcome.html',{'user':user})
                else:
                    messages.warning(request,'帐号禁用，联系管理员')
            else:
                messages.error(request,'登录失败，请检查帐号密码')
    login_form=LoginForm()
    return render(request,'account/login.html',{'login_form':login_form})

def user_register(request):
    if request.method == 'POST':
        register_form=RegisterForm(request.POST)
        if register_form.is_valid():
            cd= register_form.cleaned_data
            new_user=register_form.save(commit=False)
            new_user.set_password(cd['password'])
            new_user.is_active=False
            new_user.save()
            profileuser = ProfileUser.objects.create(user=new_user)
            messages.success(request,'注册成功，验证邮箱')
            global email_yzm
            email_yzm=email_confirm(cd['email'],'yzm')
            return render(request,'account/register_confirm.html',{'new_user':new_user})
    else:
        register_form=RegisterForm()
        return render(request,'account/register.html',{'register_form':register_form})

def register_confirm(request):
    if request.method == 'POST':
        cd=request.POST.get('email_yzm')
        name=request.POST.get('user')
        if int(cd)==email_yzm:
            user=User.objects.get(username=name)
            user.is_active=True
            user.save()
            messages.success(request, '注册成功')
            return  render(request,'account/register_done.html',{'username':name})

def password_reset(request):
    if request.method=='POST':
        email_form=EmailForm(request.POST)
        if email_form.is_valid():
            cd=email_form.cleaned_data
            email=cd['email']
            email_confirm(email,'reset')
            messages.success(request,'邮件发送成功，请查收您的邮箱')
            return HttpResponseRedirect('/account')
    else:
        email_form=EmailForm()
        return render(request,'account/password_reset.html',{'email_form':email_form})

def password_reset_confirm(request,token,tuuid):
    email=base64.b64decode(token).decode('utf-8')
    per_str = email + 'reset'
    per_id=uuid.uuid3(uuid.NAMESPACE_DNS,per_str)
    if request.method=='POST':
        password_form=PasswordForm(request.POST)
        if password_form.is_valid():
            cd=password_form.cleaned_data
            if cd['password']==cd['password2']:
                user=User.objects.get(email=email)
                user.set_password(cd['password'])
                user.save()
                messages.success(request,'重置密码成功')
                return HttpResponseRedirect('/account/login')
            else:
                messages.error(request,'前后两次密码不一致')
                password_form = PasswordForm()
                return render(request, 'account/password_reset_confirm.html',
                              {'password_form': password_form, 'email': email})
    else:
        if str(per_id)== str(tuuid):
            password_form=PasswordForm()
            return render(request,'account/password_reset_confirm.html',{'password_form':password_form,'email':email})
        else:
            return HttpResponse('404，该页面不存在')

@login_required
def password_change(request):
    if request.method == 'POST':
        user_form=LoginForm(request.POST)
        password_form = PasswordForm()
        if user_form.is_valid():
            cd = user_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                messages.success(request,'验证成功')
                return render(request, 'account/password_change_set.html', {'is_confirm':True,'password_form':password_form, 'user':user})
                # return HttpResponseRedirect('set',{'is_confirm:True'})
            else:
                user_form = LoginForm()
                messages.error(request,'验证失败，用户名或者密码错误')
                return render(request, 'account/password_change.html', {'user_form': user_form})
    else:
        user_form=LoginForm()
        return render(request, 'account/password_change.html', {'user_form':user_form})

@login_required
def password_change_set(request):
    if request.method=='POST':
        password_form=PasswordForm(request.POST)
        if password_form.is_valid():
            cd=password_form.cleaned_data
            if cd['password'] == cd['password2']:
                request.user.set_password(cd['password'])
                request.user.save()
                messages.success(request, '修改密码成功')
                return HttpResponseRedirect('/account/login')
            else:
                messages.error(request, '前后两次密码不一致')
                password_form = PasswordForm()
                return render(request, 'account/password_change_set.html',
                              {'is_confirm':True,'password_form':password_form, 'user':request.user})

@login_required
def user_info(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileUserEditForm(instance=request.user.profileuser,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            cd1=user_form.cleaned_data
            cd2=profile_form.cleaned_data
            print(cd2)
            if cd1 or cd2:
                user_form.save()
                profile_form.save()
                messages.success(request,'完善信息成功')
        else:
            messages.error(request,'信息有误，请检查数据')
        user=request.user
        return render(request,'account/user_info.html',{'user_form':user_form,'profile_form':profile_form,'user':user})

    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileUserEditForm(instance=request.user.profileuser)
        user=request.user
        return render(request,'account/user_info.html',{'user_form':user_form,'profile_form':profile_form,'user':user})
