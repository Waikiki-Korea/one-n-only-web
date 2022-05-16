from django.contrib import admin
# from .models import TestInfo
from .models import OnoUser
from .models import Collection
from .models import Token
from .models import TempImage

# class TestInfoAdmin(admin.ModelAdmin):
    # search_fields = ['user_id', 'image']

class OnoUserAdmin(admin.ModelAdmin):
    search_fields = ['id', 'username']

class CollectionAdmin(admin.ModelAdmin):
    search_fields = ['id', 'title']

class TokenAdmin(admin.ModelAdmin):
    search_fields = ['id', 'ipfs_path']

class TempImageAdmin(admin.ModelAdmin):
    search_fields = ['id', 'image']

# admin.site.register(TestInfo, TestInfoAdmin)
admin.site.register(OnoUser, OnoUserAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(TempImage, TempImageAdmin)
# Register your models here.
