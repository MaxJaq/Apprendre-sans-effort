from django.urls import path
from pages.views import home_view, contact_view
from tests.views import (
	test_create_view,
	test_standard_create_view,
	test_mcq_create_view,
	test_display_view,
	test_mcq_display_view,
	test_pass_view,
	test_mcq_pass_view,
	tests_list_teacher_view,
	tests_list_student_view,
	tests_history_view,
	tests_analysis_view,
    dashboard_view,
	test_mcqtest_create_view,
	test_mcqtest_display_view,
	test_mcqtest_pass_view,
)

app_name = 'tests'

urlpatterns = [
	# Teacher
	path('manage/create/', test_create_view, name='Create test'),
	path('manage/create/standard/', test_standard_create_view, name='Create standard test'),
	path('manage/create/mcq/', test_mcq_create_view, name='Create mcq test'),
	path('manage/create/mcqtest/', test_mcqtest_create_view, name='Create MCQTest test'),
	path('manage/display/<str:input_id_test>/', test_display_view, name='Display test'),
	path('manage/display/mcq/<str:input_id_test>/', test_mcq_display_view, name='Display mcq test'),
	path('manage/display/mcqtest/<str:input_id_test>/', test_mcqtest_display_view, name='Display MCQTest test'),
	path('manage/list/', tests_list_teacher_view, name='List tests teacher'),
	path('manage/analysis/', tests_analysis_view, name='Analyse tests'),
    path('manage/dashboard/', dashboard_view,name='Dashboard'),

	# Student
	path('pass/<str:input_id_test>', test_pass_view, name='Pass test'),
	path('pass/mcq/<str:input_id_test>', test_mcq_pass_view, name='Pass test mcq'),
	path('pass/mcqtest/<str:input_id_test>', test_mcqtest_pass_view, name='Pass test mcqtest'),
	path('pass/list/', tests_list_student_view, name='List tests student'),
	path('pass/history/', tests_history_view, name='Tests history'),
]
