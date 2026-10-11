from django.db import models

class Branch(models.Model):
    branch_name=models.CharField(max_length=50)
    branch_id=models.CharField(max_length=20)
    section=models.CharField(max_length=20)
    creation_date=models.DateField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.branch_name} - {self.section}"

class Subject(models.Model):
    subject_name=models.CharField(max_length=50)
    subject_id=models.CharField(max_length=20)
    creation_date=models.DateField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} - {self.subject_id}"

class Student(models.Model):
    GENDER_CHOICES=(('Male','Male'),
                    ('Female','Female'),
                    )

    name=models.CharField(max_length=50)
    reg_id=models.CharField(max_length=20)
    email_id=models.CharField(max_length=50)
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES)
    dob=models.CharField(max_length=30)
    student_branch=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    reg_date=models.DateField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)
    status=models.IntegerField(default=1)

    def __str__(self):
        return self.name


#subject=models.ForeignKey(Subject,on_delete=models.SET_NULL)

class Subjects(models.Model):
    student_branch=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    status=models.IntegerField(default=1)
    creation_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_branch} - {self.subject}"

class Result(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    student_branch=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    subject=models.ForeignKey(Subject,on_delete=models.SET_NULL,null=True)
    marks=models.IntegerField()
    creation_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}"

class Notice(models.Model):
    title=models.CharField(max_length=100)
    detail=models.TextField()
    posting_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title