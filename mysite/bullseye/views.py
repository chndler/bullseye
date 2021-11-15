from django.shortcuts import render

# User added imports
from django.http import HttpResponse
from .models import *
from django.template import loader
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404

# Create your views here.

# index view should be dashboard, somehow enable url redirect?
def dashboard(request):
    student_list = Student.objects.order_by('last_name')
    evaluation_list = Evaluation.objects.all()
    school_list = School.objects.all()
    district_list = District.objects.all()
    template = loader.get_template('bullseye/dashboard.html')
    context = {
        'student_list': student_list,
        'evaluation_list': evaluation_list,
        'school_list': school_list,
        'district_list': district_list,
    }
    return HttpResponse(template.render(context, request))

def school_index(request):
    # TODO Fill in student view
    school_list = School.objects.all()
    template = loader.get_template('bullseye/school-index.html')
    context = {
        'school_list': school_list,
    }
    return HttpResponse(template.render(context, request))

def district_index(request):
    # TODO Fill in student view
    district_list = District.objects.all()
    template = loader.get_template('bullseye/district-index.html')
    context = {
        'district_list': district_list,
    }
    return HttpResponse(template.render(context, request))

def district(request, district_id):
    # TODO Fill in school view
    # TODO Move note assignment into it's own try/catch!
    try:
        district = District.objects.get(id=district_id)
    except ObjectDoesNotExist:
        print("School with id", district_id, "does not exist")
        district = None
    try:
        schools = district.schools.order_by('name')
    except ObjectDoesNotExist:
        print("No schools exist for district with id ", district_id)
        schools = None
    # try:
    #     evaluations = Evaluation.objects.filter(student_id=student.id)
    # except ObjectDoesNotExist:
    #     print("No evaluations exist for student with id ", school_id)
    #     evaluations = None
    template = loader.get_template('bullseye/district-detail.html')
    context = {
        'district': district,
        'schools': schools,
        'district_id': district_id,
    }
    return HttpResponse(template.render(context, request))

def school(request, school_id):
    # TODO Fill in school view
    # TODO Move note assignment into it's own try/catch!
    # try:
    #     school = School.objects.get_object_or_404(id=school_id)
    # except ObjectDoesNotExist:
    #     print("School with id", school_id, "does not exist")
    #     school = None
    school = get_object_or_404(School, id=school_id)
    try:
        students = school.students.order_by('last_name')
    except ObjectDoesNotExist:
        # print("No students exist for school with id ", school_id)
        students = None
    # students = get_list_or_404(school.students.order_by('last_name'))
    # try:
    #     evaluations = Evaluation.objects.filter(student_id=student.id)
    # except ObjectDoesNotExist:
    #     print("No evaluations exist for student with id ", school_id)
    #     evaluations = None
    template = loader.get_template('bullseye/school-detail.html')
    context = {
        'school': school,
        'students': students,
        'school_id': school_id,
    }
    return HttpResponse(template.render(context, request))

def student_index(request):
    # TODO Fill in student view
    student_list = Student.objects.all()
    template = loader.get_template('bullseye/student-index.html')
    context = {
        'student_list': student_list,
    }
    return HttpResponse(template.render(context, request))

def student(request, student_id):
    # TODO Fill in student view
    # TODO Move note assignment into it's own try/catch!
    try:
        student = Student.objects.get(id=student_id)
    except ObjectDoesNotExist:
        print("Student with id ", student_id, "does not exist")
        student = None
    try:
        notes = student.notes.order_by('-date_modified')
    except ObjectDoesNotExist:
        print("No notes exist for student with id ", student_id)
        notes = None
    try:
        evaluations = Evaluation.objects.filter(student_id=student.id)
    except ObjectDoesNotExist:
        print("No evaluations exist for student with id ", student_id)
        evaluations = None
    template = loader.get_template('bullseye/student-detail.html')
    context = {
        'student': student,
        'notes': notes,
        'evaluations': evaluations,
        'student_id': student_id,
    }
    return HttpResponse(template.render(context, request))

def evaluation_index(request):
    # TODO Fill in student view
    evaluation_list = Evaluation.objects.order_by('due_date')
    template = loader.get_template('bullseye/evaluation-index.html')
    context = {
        'evaluation_list': evaluation_list,
    }
    return HttpResponse(template.render(context, request))

def evaluation(request, evaluation_id):
    # TODO Fill in student view
    try:
        eval = Evaluation.objects.get(id=evaluation_id)
        notes = eval.notes.all()
    except ObjectDoesNotExist:
        print("Evaluation/notes with id=", evaluation_id, "does not exist")
        eval = None
        notes = None
    template = loader.get_template('bullseye/evaluation-detail.html')
    context = {
        'eval': eval,
        'notes': notes,
        'eval_id': evaluation_id,
    }
    return HttpResponse(template.render(context, request))

def note(request, note_id):
    try:
        note = Note.objects.get(id=note_id)
    except ObjectDoesNotExist:
        print("Note with id", note_id, "does not exist")
        note = None
    template = loader.get_template('bullseye/note.html')
    context = {
        'note': note,
        'note_id': note_id,
    }
    return HttpResponse(template.render(context, request))
