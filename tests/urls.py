from django.urls import path
from django.contrib.auth import views as auth_views
from pages.views import home_view, contact_view
from tests.views import (
	login_view,
	logout_view,
	register_view,
	
	test_create_view,
	DynMCQTest_menu_view,
	DynMCQquestion_select_menu_view,
	DynMCQquestion_create_view,
	Dynquestion_create_view,
	DynMCQanswer_create_view,
	
	Manage_questions_view,
	Question_reallocation_view,
	Add_difficulty_view,
	Add_difficulty_question_view,
	
	Edit_DynMCQquestion_view,
	Edit_Dynquestion_view,
	Edit_DynMCQanswer_view,
	Delete_DynMCQquestion_view,
	Delete_Dynquestion_view,
	Delete_DynMCQanswer_view,
	Add_DynMCQquestion_view,
	Add_DynMCQanswer_view,
	Add_Dynquestion_view,
	
	pass_dynMCQtest_display_view,
	DynMCQtest_display_view,
	
	pass_testslist_teacher_view,
	DynMCQtest_pass_view,
	DynMCQTest_pass_menu_view,
	
	tests_list_teacher_view,
	tests_list_student_view,
	tests_history_view,
	dashboard_view,
	statistics_view,
	
	launch_view,
	launch_specific_dynmcq_view,
	in_launch_specific_dynmcq_view,
	in_launch_mcq_stop_test,
)

app_name = 'tests'

urlpatterns = [
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
	path('register/', register_view, name='register'),

	# Teacher
	path('manage/create/', test_create_view, name='Create test'),
	path('manage/create/dynmcqtestmenu/', DynMCQTest_menu_view, name='Create DynMCQTest Menu'),
	path('manage/create/dynmcqtestselectqmenu/<str:input_id_test>/', DynMCQquestion_select_menu_view, name='SelectMenu DynMCQquestion'),
	path('manage/create/dynmcqtestmcqquestion/<str:input_q_num>/', DynMCQquestion_create_view, name='Create DynMCQquestion'),
	path('manage/create/dynmcqtestquestion/<str:input_q_num>/', Dynquestion_create_view, name='Create Dynquestion'),
	path('manage/create/dynmcqtestanswer/<str:input_q_num>/', DynMCQanswer_create_view, name='Create DynMCQanswers'),

	path('manage/create/managequestions', Manage_questions_view, name='Manage Questions'),
	path('manage/create/question_reallocation/<str:input_id_test>/', Question_reallocation_view, name='Question_reallocation'),
	path('manage/create/add_difficulty/<str:input_q_num>/', Add_difficulty_view, name='Add Difficulty'),
	path('manage/create/add_difficulty_question/<str:input_q_num>/', Add_difficulty_question_view, name='Add Difficulty question'),
	
	path('manage/create/dynmcqtestaddmcqquestion/', Add_DynMCQquestion_view, name='AddQuestion DynMCQquestion'),
	path('manage/create/dynmcqtestaddquestion/', Add_Dynquestion_view, name='AddQuestion Dynquestion'),
	path('manage/create/dynmcqtestaddanswer/<str:input_q_num>', Add_DynMCQanswer_view, name='AddAnswer DynMCQanswer'),
	path('manage/edit/dynmcqtestmcqquestion/<str:input_q_num>', Edit_DynMCQquestion_view, name='Edit DynMCQquestion'),
	path('manage/edit/dynmcqtestquestion/<str:input_q_num>', Edit_Dynquestion_view, name='Edit Dynquestion'),
	path('manage/edit/dynmcqtestanswer/<str:input_q_num>/<str:input_ans_num>', Edit_DynMCQanswer_view, name='Edit DynMCQanswer'),
	path('manage/delete/dynmcqtestmcqquestion/<str:input_q_num>', Delete_DynMCQquestion_view, name='Delete DynMCQquestion'),
	path('manage/delete/dynmcqtestquestion/<str:input_q_num>', Delete_Dynquestion_view, name='Delete Dynquestion'),
	path('manage/delete/dynmcqtestanswer/<str:input_q_num>/<str:input_ans_num>', Delete_DynMCQanswer_view, name='Delete DynMCQanswer'),
	
	path('manage/display/passdynMCQtest/<str:input_id_test>/<str:input_id_student>/<int:input_attempt>/', pass_dynMCQtest_display_view, name='Display pass dynmcqtest'),
	path('manage/display/dynmcqtest/<str:input_id_test>/', DynMCQtest_display_view, name='Display DynMCQtest'),
	
	path('manage/list/test', tests_list_teacher_view, name='List tests teacher'),
	path('manage/list/pass_test', pass_testslist_teacher_view, name='List pass tests teacher'),
	path('manage/dashboard/', dashboard_view, name='Dashboard'),
	path('manage/statistics/<str:input_id_test>/', statistics_view, name='Statistics'),
	
	path('manage/launch/', launch_view, name='Launch'),
	path('manage/launch/mcqdyn/<str:input_id_test>/', launch_specific_dynmcq_view, name='Launch Specific McqDyn'),
	path('manage/inlaunch/mcqdyn/<str:input_id_test>/', in_launch_specific_dynmcq_view, name='In Launch Specific DynMcq'),
	path('manage/stopinlaunch/mcqdyn/<str:input_id_test>/', in_launch_mcq_stop_test, name='Stop mcq launch'),

	# Student
	path('pass/dynmcqtest/<str:input_id_test>/<str:input_id_student>/<int:input_attempt>', DynMCQtest_pass_view, name='Pass dynmcqtest'),
	path('pass/menudynmcqtest/<str:input_id_test>', DynMCQTest_pass_menu_view, name='Menu Pass dynmcqtest'),
	path('pass/list/', tests_list_student_view, name='List tests student'),
	path('pass/history/', tests_history_view, name='Tests history'),
]
