# models.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=100, blank=True, null=True)
    ops_user = models.BooleanField(default=False)
    signup_url = models.CharField(max_length=100, blank=True, null=True)

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=[('pptx', 'PPTX'), ('docx', 'DOCX'), ('xlsx', 'XLSX')])
    download_link = models.CharField(max_length=100, blank=True, null=True)
