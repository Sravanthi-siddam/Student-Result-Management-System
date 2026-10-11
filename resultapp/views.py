from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# Create your views here.

def index(request):
    notices=Notice.objects.all().order_by('-id')
    return render(request,'index.html',locals())

def notice_detail(request,notice_id):

    notices=get_object_or_404(Notice,id=notice_id)
    return render(request,'notice_detail.html',locals())



def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    error=None
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)

        if user is not None and user.is_superuser:
            login(request,user)
            return redirect('admin_dashboard')
        else:
            error="Invalid or Not Authorised"

    return render(request,'admin_login.html',locals())

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin-login')
    total_students=Student.objects.count()
    total_subjects=Subject.objects.count()
    total_branches=Branch.objects.count()
    total_results=Result.objects.values('student').distinct().count()

    return render(request,'admin_dashboard.html',locals())

def admin_logout(request):
    logout(request)
    return render(request,'admin_logout.html')


@login_required
def create_branch(request):
    if request.method=='POST':
        try:
            branch_name=request.POST.get('branchname')
            branch_id=request.POST.get('branch_id')
            section=request.POST.get('section')
            Branch.objects.create(branch_name=branch_name,branch_id=branch_id,section=section)
            messages.success(request,"Branch created sucessfully")
            return redirect('create_branch')

        except Exception as e:
            messages.error(request,f"Something went Wrong: {str(e)}")
            return redirect('create_branch')
    return render(request,'create_branch.html')



@login_required
def manage_branches(request):
    branches=Branch.objects.all()
    if request.GET.get('delete'):
        try:
            class_no=request.GET.get('delete')
            class_obj=get_object_or_404(Branch,pk=class_no)
            class_obj.delete()
            messages.success(request,"Class deleted Sucessfully")
        except Exception as e:
            messages.error(request,f"Somrthing went wrong: {str(e)}")
            return redirect('create_branch')

    return render(request,'manage_branches.html',locals())

@login_required
def edit_branch(request, id):
    class_obj = get_object_or_404(Branch, id=id)

    if request.method == 'POST':
        branch_name = request.POST.get('branchname')
        branch_id = request.POST.get('branch_id')
        section = request.POST.get('section')

        try:
            class_obj.branch_name = branch_name
            class_obj.branch_id = branch_id
            class_obj.section = section
            class_obj.save()

            messages.success(request, "Branch updated successfully")
            return redirect('manage_branches')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('edit_branch', id=id)

    return render(request, 'edit_branch.html', {'class_obj': class_obj})





@login_required
def add_subject(request):
    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subjectname')
            subject_id = request.POST.get('subjectcode')

            Subject.objects.create(
                subject_name=subject_name,
                subject_id=subject_id
            )

            messages.success(request, "Subject Added successfully")
            return redirect('add_subject')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('add_subject')

    return render(request, 'add_subject.html')


@login_required
def manage_subject(request):
    subjects = Subject.objects.all()
    if request.GET.get('delete'):
        try:
            subject_id = request.GET.get('delete')
            subject = get_object_or_404(Subject, id=subject_id)
            subject.delete()
            messages.success(request, "Subject deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manage_subject')
    return render(request, 'manage_subject.html', {'subjects': subjects})


@login_required
def edit_subject(request, id):
    subject = get_object_or_404(Subject, id=id)

    if request.method == 'POST':
        try:
            subject_name = request.POST.get('subjectname')
            subject_id = request.POST.get('subjectcode')

            subject.subject_name = subject_name
            subject.subject_id = subject_id

            subject.save()

            messages.success(request, "Subject updated successfully")
            return redirect('manage_subject')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('edit_subject', id=id)

    return render(request, 'edit_subject.html', {'subject': subject})


@login_required
def add_subject_combination(request):
    branches = Branch.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        try:
            branch_id = request.POST.get('branch')
            subject_id = request.POST.get('subject')

            print("Branch ID:", branch_id)
            print("Subject ID:", subject_id)

            branch = get_object_or_404(Branch, id=branch_id)
            subject = get_object_or_404(Subject, id=subject_id)

            Subjects.objects.create(
                student_branch=branch,
                subject=subject
            )

            messages.success(request, "Subject combination added successfully")
            return redirect('add_subject_combination')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('add_subject_combination')

    return render(request, 'add_subject_combination.html', {
        'branches': branches,
        'subjects': subjects
    })


@login_required
def manage_subject_combination(request):
    combinations = Subjects.objects.all()

    if request.GET.get('delete'):
        try:
            combination_id = request.GET.get('delete')

            combination = get_object_or_404(
                Subjects,
                id=combination_id
            )
            combination.delete()
            messages.success(
                request,
                "Subject combination deleted successfully"
            )
        except Exception as e:
            messages.error(
                request,
                f"Something went wrong: {str(e)}")

        return redirect('manage_subject_combination')

    return render(
        request,
        'manage_subject_combination.html',
        {
            'combinations': combinations
        }
    )

@login_required
def edit_subject_combination(request, id):

    combination = get_object_or_404(
        Subjects,
        id=id)
    branches = Branch.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        try:
            branch_id = request.POST.get('branch')
            subject_id = request.POST.get('subject')

            branch = get_object_or_404(
                Branch,
                id=branch_id
            )

            subject = get_object_or_404(
                Subject,
                id=subject_id
            )

            combination.student_branch = branch
            combination.subject = subject

            combination.save()

            messages.success(
                request,
                "Subject combination updated successfully"
            )

            return redirect('manage_subject_combination')

        except Exception as e:

            messages.error(
                request,
                f"Something went wrong: {str(e)}"
            )

            return redirect(
                'edit_subject_combination',
                id=id
            )

    return render(
        request,
        'edit_subject_combination.html',
        {
            'combination': combination,
            'branches': branches,
            'subjects': subjects
        }
    )

@login_required
def add_student(request):
    branches = Branch.objects.all()

    if request.method == 'POST':
        try:
            name = request.POST.get('fullname')
            reg_id = request.POST.get('regid')
            email_id = request.POST.get('emailid')
            gender= request.POST.get('gender')
            dob = request.POST.get('dob')
            branch_id= request.POST.get('branch')
            student_branch=Branch.objects.get(id=branch_id)

            Student.objects.create(name=name,reg_id=reg_id,email_id=email_id,gender=gender,dob=dob,student_branch=student_branch )
            messages.success(request, "Student data added successfully")
            return redirect('add_student')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('add_student')
    return render(request, 'add_student.html', {
        'branches': branches})

@login_required
def manage_students(request):
    students = Student.objects.all()
    if request.GET.get('delete'):
        try:
            student_id = request.GET.get('delete')
            student = get_object_or_404(Student,id=student_id)
            student.status = 0
            student.save()
            messages.success(request,"Student deactivated successfully")
        except Exception as e:
            messages.error(
                request,
                f"Something went wrong: {str(e)}"
            )

        return redirect('manage_students')

    return render(request, 'manage_students.html', {
        'students': students
    })


@login_required
def edit_student(request, student_id):
    student_obj = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        try:
            student_obj.name = request.POST.get('fullname')
            student_obj.reg_id = request.POST.get('regid')
            student_obj.email = request.POST.get('emailid')
            student_obj.gender= request.POST.get('gender')
            student_obj.dob= request.POST.get('dob')
            student_obj.status= request.POST.get('status')
            student_obj.save()
            messages.success(request, "Student info updated successfully")
            return redirect('manage_subject')

        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
            return redirect('manage_students', id=id)

    return render(request, 'edit_student.html',locals())

@login_required
def add_notice(request):
    if request.method=='POST':
        try:
            title=request.POST.get('title')
            details=request.POST.get('details')

            Notice.objects.create(title=title,detail=details)
            messages.success(request, "Notice added successfully")
            
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('add_notice')
    return render(request, 'add_notice.html',locals())


@login_required
def manage_notice(request):
    notices=Notice.objects.all()
    if request.GET.get('delete'):
        try:
            notice_id = request.GET.get('delete')
            notice_obj = get_object_or_404(Notice, id=notice_id)
            notice_obj.delete()
            messages.success(request, "Notice deleted successfully")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")
        return redirect('manage_notice')
    return render(request, 'manage_notice.html',locals())


@login_required
def add_result(request):
    branches = Branch.objects.all()
    if request.method == 'POST':
        try:
            branch_id = request.POST.get('branch')
            student_id = request.POST.get('student_id')
            print("BRANCH ID:", branch_id)
            print("STUDENT ID:", student_id)
            if not student_id:
                messages.error(request, "Please select a student.")
                return redirect('add_result')
            if not branch_id:
                messages.error(request, "Please select a branch.")
                return redirect('add_result')

            student = get_object_or_404(Student,id=student_id)
            branch = get_object_or_404(Branch,id=branch_id)
            subject_combinations = Subjects.objects.filter(student_branch=branch,status=1)

            for combination in subject_combinations:

                subject = combination.subject

                marks = request.POST.get(
                    f'marks_{subject.id}'
                )
                if marks:
                    Result.objects.create(student=student,student_branch=branch,subject=subject,marks=marks)
            messages.success(
                request,
                "Result added successfully"
            )

            return redirect('add_result')

        except Exception as e:
            messages.error(
                request,
                f"Something went wrong: {str(e)}"
            )

            return redirect('add_result')
    return render(
        request,
        'add_result.html',
        {'branches': branches}
    )

'''@login_required
def view_student_results(request, id):
    student = get_object_or_404(Student, id=id)
    results = Result.objects.filter(student=student)
    return render(request, 'view_student_results.html', { 'student': student,'results': results})'''

from django.http import JsonResponse

@login_required
def get_student_subjects(request):
    branch_id = request.GET.get('branch_id')
    if not branch_id:
        return JsonResponse({
            'students': [],
            'subjects': []
        })

    students = Student.objects.filter(
        student_branch_id=branch_id,
        status=1
    ).values('id','name','reg_id')
    students = list(students)
    subject_combinations = Subjects.objects.filter(student_branch_id=branch_id,status=1).select_related('subject')
    subjects = []
    for combination in subject_combinations:

        subjects.append({
            'id': combination.subject.id,
            'name': combination.subject.subject_name,
            'code': combination.subject.subject_id
        })

    return JsonResponse({
        'students': students,
        'subjects': subjects
    })


@login_required
def manage_result(request):
    results=Result.objects.select_related('student','student_branch').all()
    students = {}
    for res in results:
        stu_id=res.student.reg_id
        if stu_id not in students:
            students[stu_id]={
                'student':res.student,
                'branch':res.student_branch,
                'reg_date':res.student.reg_date,
                'status':res.student.status,
            }
    return render(request, 'manage_result.html',{'results': students.values()})

@login_required
def edit_result(request,stdid):
    student=get_object_or_404(Student,id=stdid)
    results=Result.objects.filter(student=student)
    if request.method=='POST':
        ids=request.POST.getlist('id[]')
        marks=request.POST.getlist('marks[]')

        for i in range(len(ids)):
            result_obj=get_object_or_404(Result,id=ids[i])
            result_obj.marks=marks[i]
            result_obj.save()
        messages.success(request,'Result updated sucessfully')
        return redirect('edit_result', stdid=stdid)

    return render(request, 'edit_result.html',locals())


from django.contrib.auth import update_session_auth_hash
@login_required
def change_password(request):
    if request.method=='POST':

        old_pass=request.POST.getlist('old')
        new_pass=request.POST.getlist('new')
        conf=request.POST.getlist('confirm')

        if new_pass!=conf:
            messages.error(request,'New password and confirm Password do not Match')
            return redirect('change_password')

        user=authenticate(username=request.user.username,password=old_pass)
        if user:
            user.set_password(new_pass)
            user.save()
            update_session_auth_hash(request,user)

            messages.success(request,'Password updated sucessfully')
            return redirect('change_password')
        else:
            messages.success(request,'Wrong password')
            return redirect('change_password')

    return render(request,'change_password.html',locals())

def search_result(request):
    branches=Branch.objects.all()

    return render(request,'search_result.html',locals())


'''def check_result(request):
    if request.method=='POST':
        regid=request.POST['regid']
        branch_id=request.POST['branch']

        try:
            Student.objects.get(reg_id=regid,student_branch_id=branch_id)
            results=Result.POST.filter(student=Student)

            total_marks=sum([r.marks for r in results])
            subject_count=results.count()
            max_total=subject_count*100
            percentage=(total_marks/max_total)*100 if max_total>0 else 0
            round(percentage,2)
            print("TOTAL:", total_marks)
            print("MAXIMUM:", max_total)
            print("PERCENTAGE:", percentage)

            return render(
                request,
                'student_result.html',
                {
                    'student': Student,
                    'results': results,
                    'total_marks': total_marks,
                    'maximum_marks': max_total,
                    'percentage': round(percentage, 2),
                   
                }
            )
        except Exception as e:
                messages.error(request, f"No result found for given reg id and class")
                return redirect('search_result')
    
    #return render(request,'check_result.html',locals())'''

def result_page(request):
    branches = Branch.objects.all()

    return render(
        request,'result_page.html',{'branches': branches}    )



def result_page(request):
    branches = Branch.objects.all()

    return render(
        request,
        'result_page.html',
        {'branches': branches}
    )


def check_result(request):
    branches = Branch.objects.all()
    if request.method == 'POST':
        reg_id = request.POST.get('regid')
        branch_id = request.POST.get('branch')

        try:
            student = Student.objects.get(reg_id=reg_id,student_branch_id=branch_id,status=1)
            results = Result.objects.filter(student=student
            ).select_related('subject', 'student_branch')
            if not results.exists():
                messages.error(
                    request,
                    "Result is not available for this student."
                )
                return render(
                    request,
                    'result_page.html',
                    {'branches': branches}
                )
            total_marks = sum( result.marks for result in results)
            subject_count = results.count()
            maximum_marks = subject_count * 100
            percentage = ((total_marks / maximum_marks) * 100 if maximum_marks > 0 else 0)
            result_status = "PASS"
            for result in results:
                if result.marks < 35:
                    result_status = "FAIL"
                    break
            print("TOTAL:", total_marks)
            print("MAXIMUM:", maximum_marks)
            print("PERCENTAGE:", percentage)
            print("STATUS:", result_status)

            return render(
                request,
                'student_result.html',
                {
                    'student': student,
                    'results': results,
                    'total_marks': total_marks,
                    'maximum_marks': maximum_marks,
                    'percentage': round(percentage, 2),
                    'result_status': result_status
                }
            )

        except Student.DoesNotExist:
            messages.error(
                request,
                "Student not found. Please check Registration ID and Branch." )
            return render(
                request,
                'result_page.html',
                {'branches': branches}
            )
        except Student.MultipleObjectsReturned:
            messages.error(
                request,
                "Multiple students found with this Registration ID and Branch."
            )
            return render(
                request,
                'result_page.html',
                {'branches': branches}
            )
    return render(
        request,
        'result_page.html',
        {'branches': branches}
    )


def notice_detail(request, id):
    notice = get_object_or_404(Notice, id=id)
    return render( request,'notice_detail.html',
        {'notice': notice})

@login_required
def view_student_results(request, id):
    student = get_object_or_404(Student, id=id)
    results = Result.objects.filter(student=student).select_related('subject', 'student_branch')
    return render(request,'view_student_results.html',{
            'student': student,
            'results': results
        }
    )

@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        messages.success(
            request,
            "Student deleted permanently."
        )
        return redirect('manage_students')
    return render(
        request,
        'delete_student.html',
        {'student': student}
    )
