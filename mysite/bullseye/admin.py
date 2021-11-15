from django.contrib import admin

# User added imports
from .models import District, School, Student, Evaluation, Note

class Dates(admin.ModelAdmin):
    readonly_fields = ('date_added', 'date_modified',)

# Register your models here.
admin.site.register(District, Dates)
admin.site.register(School, Dates)
admin.site.register(Student, Dates)
admin.site.register(Evaluation, Dates)
admin.site.register(Note, Dates)
