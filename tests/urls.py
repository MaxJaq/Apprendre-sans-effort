from django.urls import path
from django.contrib.auth import views as auth_views
from pages.views import home_view, contact_view
from tests.views import (
	login_view,
	logout_view,
	register_view,
	
	test_create_view,
	test_standard_create_view,
	test_mcq_create_view,
	DynTest_create_view,
	test_mcqtest_create_view,
	DynTest_menu_view,
	DynMCQTest_menu_view,
	DynMCQquestion_select_menu_view,
	DynMCQquestion_create_view,
	DynMCQanswer_create_view,
	
	Edit_DynMCQquestion_view,
	Edit_DynMCQanswer_view,
	Delete_DynMCQquestion_view,
	Delete_DynMCQanswer_view,
	Add_DynMCQquestion_view,
	Add_DynMCQanswer_view,
	
	test_display_view,
	test_mcq_display_view,
	dyntest_display_view,
	pass_mcqtest_display_view,
	test_mcqtest_display_view,
	pass_test_display_view,
	pass_dyntest_display_view,
	pass_dynMCQtest_display_view,
	DynMCQtest_display_view,
	
	test_mcqtest_pass_view,
	test_pass_view,
	test_mcq_pass_view,
	pass_testslist_teacher_view,
	dyntest_pass_view,
	DynMCQtest_pass_view,
	DynMCQTest_pass_menu_view,
	
	tests_list_teacher_view,
	tests_list_student_view,
	tests_history_view,
	tests_analysis_view,
	dashboard_view,
	statistics_view,
	
	launch_view,
	launch_specific_dyn_view,
	launch_specific_dynmcq_view,
	in_launch_specific_dyn_view,
	in_launch_specific_dynmcq_view,
)

app_name = 'tests'

urlpatterns = [
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
	path('register/', register_view, name='register'),

	# Teacher
	path('manage/create/', test_create_view, name='Create test'),
	path('manage/create/standard/', test_standard_create_view, name='Create standard test'),
	path('manage/create/mcq/', test_mcq_create_view, name='Create mcq test'),
	path('manage/create/mcqtest/', test_mcqtest_create_view, name='Create MCQTest test'),
	path('manage/create/dyntestmenu/', DynTest_menu_view, name='Create DynTest Menu'),
	path('manage/create/dyntest/<str:input_id_test>/', DynTest_create_view, name='Create DynTest'),
	path('manage/create/dynmcqtestmenu/', DynMCQTest_menu_view, name='Create DynMCQTest Menu'),
	path('manage/create/dynmcqtestselectqmenu/<str:input_id_test>/', DynMCQquestion_select_menu_view, name='SelectMenu DynMCQquestion'),
	path('manage/create/dynmcqtestquestion/<str:input_id_test>/<str:input_q_num>', DynMCQquestion_create_view, name='Create DynMCQquestion'),
	path('manage/create/dynmcqtestanswer/<str:input_id_test>/<str:input_q_num>', DynMCQanswer_create_view, name='Create DynMCQanswers'),
	path('manage/create/dynmcqtestaddquestion/<str:input_id_test>/', Add_DynMCQquestion_view, name='AddQuestion DynMCQquestion'),
	path('manage/create/dynmcqtestaddanswer/<str:input_id_test>/<str:input_q_num>', Add_DynMCQanswer_view, name='AddAnswer DynMCQanswer'),
	
	path('manage/edit/dynmcqtestquestion/<str:input_id_test>/<str:input_q_num>', Edit_DynMCQquestion_view, name='Edit DynMCQquestion'),
	path('manage/edit/dynmcqtestanswer/<str:input_id_test>/<str:input_q_num>/<str:input_ans_num>', Edit_DynMCQanswer_view, name='Edit DynMCQanswer'),
	path('manage/delete/dynmcqtestquestion/<str:input_id_test>/<str:input_q_num>', Delete_DynMCQquestion_view, name='Delete DynMCQquestion'),
	path('manage/delete/dynmcqtestanswer/<str:input_id_test>/<str:input_q_num>/<str:input_ans_num>', Delete_DynMCQanswer_view, name='Delete DynMCQanswer'),
	
	path('manage/display/test/<str:input_id_test>/', test_display_view, name='Display test'),
	path('manage/display/dyntest/<str:input_id_test>/', dyntest_display_view, name='Display dyntest'),
	path('manage/display/mcq/<str:input_id_test>/', test_mcq_display_view, name='Display mcq test'),
	path('manage/display/mcqtest/<str:input_id_test>/', test_mcqtest_display_view, name='Display MCQTest test'),
	path('manage/display/passmcqtest/<str:input_id_test>/', pass_mcqtest_display_view, name='Display pass mcqtest'),
	path('manage/display/passtest/<str:input_id_test>/', pass_test_display_view, name='Display pass test'),
	path('manage/display/passdyntest/<str:input_id_student>/', pass_dyntest_display_view, name='Display pass dyntest'),
	path('manage/display/passdynMCQtest/<str:input_id_test>/<str:input_id_student>/<int:input_attempt>/', pass_dynMCQtest_display_view, name='Display pass dynmcqtest'),
	path('manage/display/dynmcqtest/<str:input_id_test>/', DynMCQtest_display_view, name='Display DynMCQtest'),
	
	path('manage/list/test', tests_list_teacher_view, name='List tests teacher'),
	path('manage/list/pass_test', pass_testslist_teacher_view, name='List pass tests teacher'),
	path('manage/analysis/', tests_analysis_view, name='Analyse tests'),
	path('manage/dashboard/', dashboard_view, name='Dashboard'),
	path('manage/statistics/<str:input_id_test>/', statistics_view, name='Statistics'),
	
	path('manage/launch/', launch_view, name='Launch'),
	path('manage/launch/dyn/<str:input_id_test>/', launch_specific_dyn_view, name='Launch Specific Dyn'),
	path('manage/launch/mcqdyn/<str:input_id_test>/', launch_specific_dynmcq_view, name='Launch Specific McqDyn'),
	path('manage/inlaunch/dyn/<str:input_id_test>/', in_launch_specific_dyn_view, name='In Launch Specific Dyn'),
	path('manage/inlaunch/mcqdyn/<str:input_id_test>/', in_launch_specific_dynmcq_view, name='In Launch Specific DynMcq'),

	# Student
	path('pass/<str:input_id_test>', test_pass_view, name='Pass test'),
	path('pass/mcq/<str:input_id_test>', test_mcq_pass_view, name='Pass test mcq'),
	path('pass/mcqtest/<str:input_id_test>', test_mcqtest_pass_view, name='Pass test mcqtest'),
	path('pass/dyntest/<str:input_id_test>', dyntest_pass_view, name='Pass dyntest'),
	path('pass/dynmcqtest/<str:input_id_test>/<str:input_id_student>/<int:input_attempt>', DynMCQtest_pass_view, name='Pass dynmcqtest'),
	path('pass/menudynmcqtest/<str:input_id_test>', DynMCQTest_pass_menu_view, name='Menu Pass dynmcqtest'),
	path('pass/list/', tests_list_student_view, name='List tests student'),
	path('pass/history/', tests_history_view, name='Tests history'),
]
