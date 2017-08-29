from django.contrib import admin
from .models import ProfileUser
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user','birth','come_from','photo']

admin.site.register(ProfileUser,ProfileAdmin)