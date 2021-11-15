# User added URLs.py file

from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # example bullseye.com/districts/
    path('districts/', views.district_index, name='district_index'),
    # example bullseye.com/districts/e3044df8-945d-4061-8169-2731fc75323c
    path('districts/<uuid:district_id>/', views.district, name='district'),
    # example bullseye.com/schools/
    path('schools/', views.school_index, name='school_index'),
    # example bullseye.com/schools/e3044df8-945d-4061-8169-2731fc75323c
    path('schools/<uuid:school_id>/', views.school, name='school'),
    # example: bullseye.com/students/
    path('students/', views.student_index, name='student_index'),
    # example: bullseye.com/students/2
    path('students/<uuid:student_id>/', views.student, name='student'),
    # example: bullseye.com/evaluations/
    path('evaluations/', views.evaluation_index, name='evaluation_index'),
    # example: bullseye.com/evaluations/e3044df8-945d-4061-8169-2731fc75323c
    path('evaluations/<uuid:evaluation_id>/', views.evaluation, name='evaluation'),
    # example: bullseye.com/notes/e3044df8-945d-4061-8169-2731fc75323c
    path('notes/<uuid:note_id>/', views.note, name='note'),
]
