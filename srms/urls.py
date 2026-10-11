"""
URL configuration for srms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from resultapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='home'),
    path('admin-login',admin_login,name="admin-login"),
    path('admin_dashboard',admin_dashboard,name="admin_dashboard"),
    #path('admin_base',admin_base,admin_base)
    path('create_branch',create_branch,name='create_branch'),
    path('admin_logout',admin_logout,name='admin_logout'),
    path('manage_branches',manage_branches,name='manage_branches'),
    path('edit_branch/<int:id>',edit_branch, name='edit_branch'),
    path('add_subject',add_subject,name='add_subject'),
    #path('manage_subject',manage_subject,name=manage_subject)
    path('manage_subject', manage_subject, name='manage_subject'),
    path('edit_subject/<int:id>', edit_subject, name='edit_subject'),
    path('add_subject_combination',add_subject_combination,name='add_subject_combination'),
    path('manage_subject_combination',manage_subject_combination,name='manage_subject_combination'),
    path('edit_subject_combination/<int:id>',edit_subject_combination,name='edit_subject_combination'),
    path('add_student',add_student,name='add_student'),
    path('manage_students',manage_students,name='manage_students'),
    path('edit_student/<int:student_id>',edit_student,name='edit_student'),
    path('add_notice',add_notice,name='add_notice'),
    path('manage_notice',manage_notice,name='manage_notice'),
    path('add_result',add_result,name='add_result'),

    path('view_student_results/<int:id>',view_student_results,name='view_student_results'),
    path('get_student_subjects/',get_student_subjects,name='get_student_subjects'),
    path('manage_result',manage_result,name='manage_result'),
    path('edit_result/<int:stdid>',edit_result,name='edit_result'),
    path('change_password',change_password,name='change_password'),
    path('search_result',search_result,name='search_result'),

    path('result_page', result_page, name='result_page'),

    path('check_result/', check_result, name='check_result'),
    #path('notice_detail/<int:notice_id>',notice_detail,name='notice_datial'),
    path(
    'notice_detail/<int:id>/',
    notice_detail,
    name='notice_detail'),
    path(
    'delete_student/<int:id>/',
    delete_student,
    name='delete_student'),
    ]
