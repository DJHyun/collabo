from django.contrib import admin
from .models import User, Money, Profile
# Register your models here.
    
admin.site.register(User,)
admin.site.register(Money,)
admin.site.register(Profile)