from rest_framework import serializers
from rest_framework.reverse import reverse

from . import models


'''
Serializer for Student
'''
class StudentSerializer(serializers.ModelSerializer):
    # Serializer method fields
    list_url = serializers.SerializerMethodField(read_only=True)
    info_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        # Meta data for StudentSerializer
        model = models.Student
        fields = [
            'list_url',
            'info_url',
            'nim',
            'name',
            'major',
            'school',
            'created_at',
            'updated_at',
        ]

    # Get all Students (List)
    def get_list_url(self, obj):
        request = self.context.get('request')
        if request: return reverse('student-list', kwargs={}, request=request)
        return None
    
    # Get detail student (Retrieve)
    def get_info_url(self, obj):
        request = self.context.get('request')
        if request: return reverse('student-info', kwargs={'pk': obj.pk}, request=request)
        return None


'''
Serializer for Course
'''
class CourseSerializer(serializers.ModelSerializer):
    # Serializer method fields
    list_url = serializers.SerializerMethodField(read_only=True)
    info_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        # Meta data for StudentSerializer
        model = models.Course
        fields = [
            'list_url',
            'info_url',
            'code',
            'name',
            'schedule',
            'created_at',
            'updated_at',
        ]

    # Get all courses (List)
    def get_list_url(self, obj):
        request = self.context.get('request')
        if request: return reverse('course-list', kwargs={}, request=request)
        return None
    
    # Get detail course (Retrieve)
    def get_info_url(self, obj):
        request = self.context.get('request')
        if request: return reverse('course-info', kwargs={'pk': obj.pk}, request=request)
        return None


'''
Serializer for StudentCourseRelation: Attendance
'''
class StudentCourseRelationSerializer(serializers.ModelSerializer):
    # Serializer method fields
    list_url = serializers.SerializerMethodField(read_only=True)
    info_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.StudentCourseRelation
        fields = [
            'list_url',
            'info_url',
            'status',
            'course',
            'student',
            'created_at',
            'updated_at',
        ]
    
    # Get all courses (List)
    def get_list_url(self, obj):
        request = self.context.get('request')
        if request: return reverse('attendance-list', kwargs={}, request=request)
        return None
    
    # Get detail course (Retrieve)
    def get_info_url(self, obj):
        request = self.context.get('request')
        if request: return reverse('attendance-info', kwargs={
                'pk': obj.pk,
                'course': obj.course.code,
                'student': obj.student.nim
                }, request=request)
        return None
