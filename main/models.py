from django.db import models
from django.contrib.auth import models as authmodels
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from os.path import basename
from datetime import datetime

from django.apps import apps
from django.contrib.auth.hashers import make_password

def user_directory_path(instance, filename):
    return f'{instance.user_id}/{filename}'

# Create your models here.

########## Global Objects ##########
class University(models.Model):
    name = models.CharField()
    country = models.CharField()
    city = models.CharField()
    portal_link = models.URLField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

class Course(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField()
    has_scholarship = models.BooleanField()
    scholarship_details = models.TextField(null=True, blank=True)
    application_fees = models.CharField()
    is_fee_wavabe = models.BooleanField(default=False, blank=True)
    required_documents = models.TextField()
    portal_link = models.URLField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

class Professor(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='professors')
    field = models.CharField()
    name = models.CharField()
    email = models.EmailField()
    mailling_guide = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)

########## Personal Objects ##########
class CustomUserManager(authmodels.UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self._create_user_object(username, email, password, **extra_fields)
        user.save(using=self._db)
        d1 = Document.objects.create(user=user, title='Academic Transcript')
        d1.save(using=self._db)
        d2 = Document.objects.create(user=user, title='Degree')
        d2.save(using=self._db)
        d3 = Document.objects.create(user=user, title='Statement of Purpose')
        d3.save(using=self._db)
        d4 = Document.objects.create(user=user, title='Research Statement')
        d4.save(using=self._db)
        d5 = Document.objects.create(user=user, title='Cover Letter')
        d5.save(using=self._db)
        d6 = Document.objects.create(user=user, title='Letters of Recomendation')
        d6.save(using=self._db)
        d7 = Document.objects.create(user=user, title='CV')
        d7.save(using=self._db)
        d8 = Document.objects.create(user=user, title='Language Certification')
        d8.save(using=self._db)
        d9 = Document.objects.create(user=user, title='Personal Identification')
        d9.save(using=self._db)
        d10 = Document.objects.create(user=user, title='GRE')
        d10.save(using=self._db)
        return user

    async def _acreate_user(self, username, email, password, **extra_fields):
        """See _create_user()"""
        user = self._create_user_object(username, email, password, **extra_fields)
        await user.asave(using=self._db)
        d1 = Document.objects.create(user=user, title='Academic Transcript')
        await d1.asave(using=self._db)
        d2 = Document.objects.create(user=user, title='Degree')
        await d2.asave(using=self._db)
        d3 = Document.objects.create(user=user, title='Statement of Purpose')
        await d3.asave(using=self._db)
        d4 = Document.objects.create(user=user, title='Research Statement')
        await d4.asave(using=self._db)
        d5 = Document.objects.create(user=user, title='Cover Letter')
        await d5.asave(using=self._db)
        d6 = Document.objects.create(user=user, title='Letters of Recomendation')
        await d6.asave(using=self._db)
        d7 = Document.objects.create(user=user, title='CV')
        await d7.asave(using=self._db)
        d8 = Document.objects.create(user=user, title='English Certification')
        await d8.asave(using=self._db)
        d9 = Document.objects.create(user=user, title='Personal Identification')
        await d9.asave(using=self._db)
        d10 = Document.objects.create(user=user, title='GRE')
        await d10.asave(using=self._db)
        return user
class User(AbstractUser):
    objects = CustomUserManager()

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(
        upload_to=user_directory_path,
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=[ 'pdf', 'jpg', 'jpeg', 'png', 'webp' ])]
        )
    title = models.CharField()
    content = models.TextField(null=True, blank=True)
    @property
    def filename(self):
        return basename(self.document.name) if self.document else ""

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(null=True, blank=True)
    documents = models.ManyToManyField(Document, blank=True, related_name='applications')
    note = models.CharField(null=True, blank=True)

class Task(models.Model):
    title = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    file = models.FileField(
        upload_to=user_directory_path,
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=[ 'pdf', 'jpg', 'jpeg', 'png', 'webp' ])]
        )
    content = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False, blank=True)
    deadline = models.DateField(null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks') 
    # placment_score = models.FloatField(default=0, blank=True)
    @property
    def filename(self):
        return basename(self.file.name) if self.file else ""
    @property
    def is_over(self):
        if not self.deadline:
            return False
        return datetime.now() > self.deadline