from django.db import models


class Student(models.Model):
    nim = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    major = models.CharField(max_length=100, default='Sistem dan Teknologi Informasi')
    school = models.CharField(max_length=100, default='STEI')

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nim} {self.name}'


class Course(models.Model):
    code = models.CharField(max_length=6, primary_key=True)
    name = models.CharField(max_length=512)
    schedule = models.DateTimeField()

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} {self.name}'
    

class StudentCourseRelation(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=False)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.course.code}_{self.student.nim}'

