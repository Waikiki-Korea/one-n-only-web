from django.db import models

# Create your models here.
class TestInfo(models.Model):
    user_id = models.CharField(max_length=20)
    user_name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=255)
    ipfs_path = models.CharField(max_length=255)
    created_date = models.DateTimeField('date created', auto_now_add=True)
    updated_date = models.DateTimeField('date updated', auto_now=True)
    etc = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name