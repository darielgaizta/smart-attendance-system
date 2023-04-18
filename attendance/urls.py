from django.urls import path

from . import views

urlpatterns = [
    # Student x Course: Attendance
    path('', views.StudentCourseRelationListCreateAPIView.as_view(), name='attendance-list'),
    path('<int:pk>/<str:course>/<int:student>/', views.StudentCourseRelationRetrieveUpdateDestroyAPIView.as_view(), name='attendance-info'),

    # Student
    path('student/', views.StudentListCreateAPIView.as_view(), name='student-list'),
    path('student/<int:pk>/', views.StudentRetrieveUpdateDestroyAPIView.as_view(), name='student-info'),

    # Course
    path('course/', views.CourseListCreateAPIView.as_view(), name='course-list'),
    path('course/<str:pk>/', views.CourseRetrieveUpdateDestroyAPIView.as_view(), name='course-info'),

]
