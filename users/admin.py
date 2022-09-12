from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Register your models here.

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff')


admin.site.register(CustomUser, CustomUserAdmin)