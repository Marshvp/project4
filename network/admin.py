from django.contrib import admin
from .models import User, Following, Posts

# Register your models here.
from django.contrib import admin

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_staff')

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'date')

@admin.register(Following)
class FollowingAdmin(admin.ModelAdmin):
    list_display = ('user_from', 'user_to', 'created')