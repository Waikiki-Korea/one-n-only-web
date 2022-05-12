from django.contrib import admin
from .models import TestInfo

class TestInfoAdmin(admin.ModelAdmin):
    search_fields = ['user_id', 'image']

admin.site.register(TestInfo, TestInfoAdmin)

# Register your models here.
