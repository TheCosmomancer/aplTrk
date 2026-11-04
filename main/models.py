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
    note = models.CharField(null=True, blank=True)

class Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='departments')
    portal_link = models.URLField()
    note = models.CharField(null=True, blank=True)

class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField()
    has_scholarship = models.BooleanField()
    scholarship_details = models.CharField(null=True, blank=True)
    application_fees = models.CharField()
    is_fee_wavabe = models.BooleanField(default=False, blank=True)
    required_documents = models.JSONField()
    note = models.CharField(null=True, blank=True)

class Professor(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='professors')
    name = models.CharField()
    email = models.EmailField()
    mailling_guide = models.CharField(null=True, blank=True)
    note = models.CharField(null=True, blank=True)

########## Personal Objects ##########
class User(AbstractUser):
    timezone = models.CharField(null=True)

class Mail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mails')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='mails')
    sdnt_high_prof_low = models.BooleanField()
    date = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    note = models.CharField(null=True, blank=True)

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(null=True, blank=True)

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(
        upload_to=user_directory_path,
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=[ 'pdf', 'odt', 'tex', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'webp' ])]
        )
    type = models.CharField()
    name = models.CharField()
    content = models.CharField(null=True, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    applications = models.ManyToManyField(Application, blank=True, related_name='documents')
    note = models.CharField(null=True, blank=True)

class Deadline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deadlines')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True, related_name='deadlines')
    deadline = models.DateTimeField()
    timezone = models.CharField()
    title = models.CharField()
    dcouments = models.ManyToManyField(Document, blank=True, related_name='deadlines')
    note = models.CharField(null=True, blank=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    document = models.FileField(
        upload_to=user_directory_path,
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=[ 'pdf', 'odt', 'tex', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'webp' ])]
        )
    content = models.CharField(null=True, blank=True)
    todo = models.BooleanField(default=True, blank=True)
    mail = models.OneToOneField(Mail, on_delete=models.CASCADE, blank=True, related_name='task')
    document = models.OneToOneField(Document, on_delete=models.CASCADE, blank=True, related_name='task')
    # placment_score = models.FloatField(default=0, blank=True)