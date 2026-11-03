from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

def user_directory_path(instance, filename):
    return f'{instance.user_id}/{filename}'

# Create your models here.

########## Global Objects ##########
class University(models.Model):
    name = models.CharField()
    country = models.CharField()
    city = models.CharField()
    note = models.CharField(null=True)

class Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')
    portal_link = models.URLField()
    note = models.CharField(null=True)

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField()
    deadline = models.DateTimeField()
    has_scholarship = models.BooleanField()
    scholarship_deadline = models.DateTimeField(null=True)
    application_fees = models.CharField()
    is_fee_wavabe = models.BooleanField()
    required_documents = models.JSONField()
    note = models.CharField(null=True)

class Professor(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='professors')
    name = models.CharField()
    email = models.EmailField()
    mailling_guide = models.CharField(null=True)
    note = models.CharField(null=True)

########## Personal Objects ##########
class User(AbstractUser):
    pass

class Mail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mails')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='mails')
    sdnt_high_prof_low = models.BooleanField()
    date = models.DateTimeField()
    content = models.TextField()
    note = models.CharField(null=True)

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField()

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(
        upload_to=user_directory_path,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=[ 'pdf', 'odf', 'tex', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'webp' ])]
        )
    type = models.CharField()
    name = models.CharField()
    content = models.CharField(null=True)
    completed = models.BooleanField(default=False)
    applications = models.ManyToManyField(Application, blank=True, related_name='documents')
    note = models.CharField(null=True)
