from rest_framework import generics

from . import models, serializers

from api.mixins import StaffEditorPermissionMixin


'''
Student: List, Create
List all students or create a new student
'''
class StudentListCreateAPIView(generics.ListCreateAPIView, StaffEditorPermissionMixin):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


'''
Student: Retrieve, Update, Destroy
Get, update, or delete a course
'''
class StudentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView, StaffEditorPermissionMixin):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


'''
Course: List, Create
List all courses or create a new course
'''
class CourseListCreateAPIView(generics.ListCreateAPIView, StaffEditorPermissionMixin):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


'''
Course: Retrieve, Update, Destroy
Get, update, or delete a course
'''
class CourseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView, StaffEditorPermissionMixin):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


'''
Student x Course: List, Create (Attendance)
List all attendance or create a new attendance
'''
class StudentCourseRelationListCreateAPIView(generics.ListCreateAPIView, StaffEditorPermissionMixin):
    queryset = models.StudentCourseRelation.objects.all()
    serializer_class = serializers.StudentCourseRelationSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


'''
Student x Course: Retrieve, Update, Destroy (Attendance)
Get, update, or delete a attendance
'''
class StudentCourseRelationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView, StaffEditorPermissionMixin):
    queryset = models.StudentCourseRelation.objects.all()
    serializer_class = serializers.StudentCourseRelationSerializer
    lookup_fields = ['pk', 'course', 'student']

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)