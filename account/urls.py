from django.conf.urls import url
from . import views

name='account'

urlpatterns=[
    url(r'^$',views.account_page,name='account_page'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'^register/$',views.user_register,name='register'),
    url(r'^register/register_confirm/$',views.register_confirm,name='register_confirm'),

    #重置密码
    url(r'^password_reset/$',views.password_reset,name='password_reset'),
    url(r'^password_reset/confirm/(?P<token>[=\w]+)/(?P<tuuid>[-\w]+)/$',views.password_reset_confirm,name='password_reset_confirm'),

    #修改密码
    url(r'^password_change/$',views.password_change,name='password_change'),
    url(r'^password_change/set/$',views.password_change_set,name='password_change_set'),

    url(r'^user_info/$',views.user_info,name='user_info'),
]