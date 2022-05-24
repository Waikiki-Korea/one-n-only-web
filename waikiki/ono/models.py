from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# https://www.webforefront.com/django/modeldatatypesandvalidation.html

# parent : default user
### id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, data_joined
# Ref. https://chagokx2.tistory.com/60
class OnoUser(AbstractUser):
    eth_address = models.CharField(max_length=255)
    collection_ids = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    symbol = models.ImageField(upload_to='user/symbol/', blank=True, null=True, default='white-image.png') # default='album_logos/no-image.jpg')

class Collection(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(OnoUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    symbol = models.ImageField(upload_to='collection/symbol/', blank=True, null=True, default='white-image.png')
    blockchain = models.PositiveIntegerField()
    token_size = models.PositiveIntegerField()
    media_type = models.PositiveIntegerField()
    contract_address = models.TextField(blank=True)
    description = models.TextField(blank=True)
    owner_address = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField('date created', auto_now_add=True)
    updated_date = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return "[collection] id: " + str(self.id) + ", title: " + self.title


class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    collection_id = models.ForeignKey(Collection, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    media_type = models.PositiveIntegerField()
    ipfs_path = models.TextField(blank=True)
    token_path = models.TextField(blank=True)
    sha256_hash = models.TextField(blank=True)
    description = models.TextField(blank=True)
    owner = models.CharField(max_length=255, blank=True)
    owner_id = models.BigIntegerField(null=True)
    owner_address = models.TextField(blank=True)
    created_date = models.DateTimeField('date created', auto_now_add=True)
    updated_date = models.DateTimeField('date updated', auto_now=True)
    token_image = models.ImageField(upload_to='collection/tokens/', blank=True, null=True, default='white-image.png')

    def __str__(self):
        return "[token] id: " + str(self.id) + ", image: " + str(self.ipfs_path)


class TempImage(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='temp/', blank=True, null=True)

    def __str__(self):
        return "[temp image] id: " + str(self.id) + ", image: " + str(self.image)

class Crawled(models.Model):
    id = models.BigAutoField(primary_key=True)
    blockchain = models.PositiveIntegerField()
    collection_id = models.CharField(max_length=255)
    collection_title = models.CharField(max_length=255)
    token_id = models.CharField(max_length=255)
    token_title = models.CharField(max_length=255)
    media_type = models.PositiveIntegerField()
    ipfs_path = models.TextField(blank=True)
    token_path = models.TextField(blank=True)
    sha256_hash = models.TextField(blank=True)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField('date created', auto_now_add=True)
    updated_date = models.DateTimeField('date updated', auto_now=True)
    blockchain = models.PositiveIntegerField()
    owner_address = models.TextField(blank=True)

class TempUrl(models.Model):
    id = models.BigAutoField(primary_key=True)
    ipfs_path = models.TextField(blank=True)

# class TestInfo(models.Model):
#     user_id = models.CharField(max_length=20)
#     user_name = models.CharField(max_length=100)
#     file_path = models.CharField(max_length=255)
#     ipfs_path = models.CharField(max_length=255)
#     created_date = models.DateTimeField('date created', auto_now_add=True)
#     updated_date = models.DateTimeField('date updated', auto_now=True)
#     etc = models.CharField(max_length=255, null=True)
#     image = models.ImageField(upload_to='images/', blank=True, null=True)

#     def __str__(self):
#         return "user_id: " + self.user_id + ", image: " + str(self.image)