from django.contrib import admin
from .models import *

# Register your models here.
from django.contrib.auth import authenticate  
from django.contrib.auth.admin import UserAdmin  
# Register your models here.  
class CustomUserAdmin(UserAdmin):  
    # add_form = CustomUserCreationForm  
    # form = CustomUserChangeForm  
    model = Users  
  
    list_display = ('email', 'is_staff', 'is_available',)  
    list_filter = ('email', 'is_staff', 'is_available',)  
    fieldsets = (  
        (None, {'fields': ('email', 'password','name','dob','contact_no','gender')}),  
        ('Permissions', {'fields': ('is_staff', 'is_available')}),  
    )  
    add_fieldsets = (  
        (None, {  
            'classes': ('wide',),  
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_available')}  
        ),  
    )  
    search_fields = ('email',)  
    ordering = ('email',)  
    filter_horizontal = ()  
  
admin.site.register(Users, CustomUserAdmin)  
admin.site.register(Chats)  
admin.site.register(ChatRoom)  