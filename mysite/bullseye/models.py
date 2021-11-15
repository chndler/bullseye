from django.db import models

# User added imports
from datetime import datetime, date, timedelta
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
import uuid
from math import floor # used to floor days-delta to get student age

# Create your models here.

class District(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)
    # TODO CHANGE ADDRESS TO address MODEL
    address = models.CharField(max_length=75, default='')
    contact_number = PhoneNumberField()
    notes = GenericRelation(
        'Note',
        related_name='district',
        related_query_name='districts',
    )

    def __str__(self):
        return self.name

class School(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    SCHOOL_TYPE_CHOICES = (
        ('Charter School', 'Charter School'),
        ('Private School', 'Private School'),
        ('Public School', 'Public School'),
    )
    school_type = models.CharField(
        max_length = 20,
        choices=SCHOOL_TYPE_CHOICES,
        default='Public School',
    )
    district = models.ForeignKey(
        District,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="schools",
        related_query_name="school",
    )
    # TODO CHANGE ADDRESS TO address MODEL
    address = models.CharField(max_length=75, default='')
    contact_number = PhoneNumberField()

    notes = GenericRelation(
        'Note',
        related_name='school',
        related_query_name='schools',
    )



    def __str__(self):
        return self.name

class Note(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=30)
    body = models.TextField()

    # Assign limits which is passed to content_type used in limit_choices_to field,
    # this limits the options from all objects to specified objects
    limits = models.Q(app_label = 'bullseye', model = 'district')
    limits = limits | models.Q(app_label = 'bullseye', model = 'school')
    limits = limits | models.Q(app_label = 'bullseye', model = 'student')
    limits = limits | models.Q(app_label = 'bullseye', model = 'evaluation')

    # Content type is used to map multiple model types to a single ForeignKey, check
    # django docs for 'contenttypes framework'
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limits,
        null=True,
        on_delete=models.PROTECT
    )
    object_id = models.CharField(max_length=50, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        # student_name = self.student.first_name + ' ' + self.student.last_name
        return self.title


class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    due_date = models.DateField(default=date.today() + timedelta(days=60))
    evaluation_type = models.CharField(max_length=100)
    student = models.ForeignKey(
        'Student',
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        related_name="evaluations",
        related_query_name="evaluation",
    )
    current_grade = models.IntegerField(null=True, blank=True)
    notes = GenericRelation(Note, related_query_name='evaluations')

    def __str__(self):
        student_name = self.student.first_name + ' ' + self.student.last_name
        return student_name + ' - ' + self.evaluation_type + ' - due ' + self.due_date.__str__()

    class Meta:
        permissions = (
            ('view_evaluation', 'Can view evaluation'),
            # The following permissions are built in natively to django-permissions
            # ('change_evaluation', 'Can change evaluation'),
            # ('delete_evaluation', 'Can delete evaluation'),
        )


class Student(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField(
        'date of birth',
        blank=False,
        default="2010-01-01",
    )
    school = models.ForeignKey(
        School,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="students",
        related_query_name="student",
    )
    # TODO CHANGE ADDRESS TO address MODEL
    mailing_address = models.CharField(max_length=75, default='', blank=True)
    contact_number = PhoneNumberField()
    LANGUAGE_PREFERENCE_CHOICES = (
        ('Arabic', 'Arabic'),
        ('Chinese', 'Chinese'),
        ('English', 'English'),
        ('French', 'French'),
        ('German', 'German'),
        ('Japanese', 'Japanese'),
        ('Portuguese', 'Portuguese'),
        ('Spanish', 'Spanish'),
        ('Urdu', 'Urdu'),
    )
    language_preference = models.CharField(
        max_length = 20,
        choices=LANGUAGE_PREFERENCE_CHOICES,
        default='English',
    )
    notes = GenericRelation(
        Note,
        related_name='student',
        related_query_name='students',
    )

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        permissions = (
            ('view_student', 'Can view student'),
        )

    # TODO build out methods
    def age(self):
        delta = date.today() - self.date_of_birth
        return floor(delta.days/365)

    # def save(self, *args, **kwargs):
    #     ct = ContentType.objects.get(app_label='bullseye', model='student')
    #     codename_view = 'can_view_%s' % (str(self).lower().replace(" ", "_"))
    #     name_view = 'Can view %s' % (self)
    #     codename_change = 'can_change_%s' % (str(self).lower().replace(" ", "_"))
    #     name_change = 'Can change %s' % (self)
    #     codename_delete = 'can_delete_%s' % (str(self).lower().replace(" ", "_"))
    #     name_delete = 'Can delete %s' % (self)
    #     perm = Permission.objects.get_or_create(codename=codename_view, name=name_view, content_type=ct)
    #     perm = Permission.objects.get_or_create(codename=codename_change, name=name_change, content_type=ct)
    #     perm = Permission.objects.get_or_create(codename=codename_delete, name=name_delete, content_type=ct)
    #     # print('can_view_%s, Can view %s' %(str(self).lower().replace(" ", "_"), self))
    #     super().save(*args, **kwargs)  # Call the "real" save() method.
