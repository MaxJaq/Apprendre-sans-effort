from django.shortcuts import render, get_object_or_404
from django.forms import formset_factory
from .forms import TestForm, PassTestForm, TestMcqForm, PassTestMcqForm, MCQTestForm, PassMCQTestForm, DynTestForm, Pass_DynTestForm,DynTestInfoForm,DynMCQTestInfoForm,DynMCQquestionForm,DynMCQanswerForm,Pass_DynMCQTestForm,DynMCQquestionForm_question,Pass_DynMCQTestInfoForm
from .models import Test_end_session, Pass_test_end_session, Test_mcq_end_session, MCQTest, Pass_MCQTest_end_session, DynTest,Pass_DynTest,DynTestInfo,DynMCQInfo,DynMCQquestion,DynMCQanswer,Pass_DynMCQTest,Pass_DynMCQTest_Info
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg


# Create your views here.
def test_create_view(request, *args, **kwargs):
	""" Show page which can then redirect toward standard and mcq creation pages """
	return render(request, 'manage_tests/test_create.html', {})


def test_standard_create_view(request):
	""" Show page to create a standard test (inputting text as answers) """
	form = TestForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = TestForm()

	context = {
		'form': form
	}
	return render(request, 'manage_tests/test_create_standard.html', context)
	
	
def DynMCQTest_menu_view(request):
	#Formulaire du DynMCQTestInfo
	form = DynMCQTestInfoForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = DynMCQTestInfoForm()
	
	#Récupération des tests
	DynMCQTestInfo_list_all = DynMCQInfo.objects.all()
			
	context = {
		'form': form,
		'DynMCQTestInfo_list_all' : DynMCQTestInfo_list_all,
	}
	return render(request, 'manage_tests/menu_dynmcqtest.html',context)
	
def DynMCQquestion_select_menu_view(request, input_id_test):
	#Récupération des informations du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	#Récupération des questions du test
	DynMCQquestionTest = DynMCQquestion.objects.filter(id_test=input_id_test)
	
	#On met les questions dans une liste
	DynMCQquestionTestList = []
	for instance in DynMCQquestionTest:
		DynMCQquestionTestList.append(instance)
		
	#S'il n'y a pas encore de questions créées, on créé autant de questions que précisé dans les informations du test
	if len(DynMCQquestionTestList) == 0:
		nb_q = 1
		while nb_q <= int(DynMCQTestInfo.nb_q) :
			DynamicMCQquestion = DynMCQquestion(id_test = input_id_test, q_num = nb_q)
			DynamicMCQquestion.save()
			nb_q += 1
		#On récupère les questions créées
		DynMCQquestionTest = DynMCQquestion.objects.filter(id_test=input_id_test)
		for instance in DynMCQquestionTest:
			DynMCQquestionTestList.append(instance)
			
	context = {
		'DynMCQquestionTestList': DynMCQquestionTestList,
		'DynMCQTestInfo': DynMCQTestInfo,
	}
	return render(request, 'manage_tests/selectmenu_dynmcqtest.html',context)
	
def DynMCQquestion_create_view(request, input_id_test, input_q_num):
	#Récupération des informations du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	#Récupération la question sélectionnée du test
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = input_q_num)
	#On récupère les réponses liées à la question
	DynMCQanswerTest = DynMCQanswer.objects.filter(id_test=input_id_test, q_num = input_q_num)
	DynMCQanswerTest_List = []
	empty_question = True
	empty_answer = True
	form = 0
	#Si la question n'a pas encore été "remplie", on affiche le formulaire de la question 
	if DynMCQquestionTest.q_text == "":
		form = DynMCQquestionForm(request.POST, instance = DynMCQquestionTest)
		if form.is_valid():
			form.save()
			form = DynMCQquestionForm()
			empty_question = False
	#Si la question a été rempli, on teste s'il y a des réponses déjà remplies pour les afficher 
	else:
		empty_question = False
		for instance in DynMCQanswerTest:
			DynMCQanswerTest_List.append(instance)
		if len(DynMCQanswerTest_List) != 0:
			empty_answer = False
			
	context = {
		'form': form,
		'empty_question': empty_question,
		'empty_answer': empty_answer,
		'DynMCQquestionTest' : DynMCQquestionTest,
		'DynMCQanswerTest_List':DynMCQanswerTest_List,
		'DynMCQTestInfo':DynMCQTestInfo
	}
	return render(request, 'manage_tests/test_create_dynmcqquestion.html',context)
	
def DynMCQanswer_create_view(request, input_id_test, input_q_num):
	#Récupération des informations du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	#Récupération la question sélectionnée du test
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = input_q_num)
	
	empty_answer = True
	#Récupération des réponses du test
	DynMCQanswerTest = DynMCQanswer.objects.filter(id_test = input_id_test, q_num = input_q_num)
	DynMCQanswerTest_List = []
	for instance in DynMCQanswerTest:
		DynMCQanswerTest_List.append(instance)
		
	if len(DynMCQanswerTest_List) != 0:
		empty_answer = False
	
	nb_answers = DynMCQquestionTest.nb_ans
	
	form = 0
	
	#S'il n'y a pas de réponses encore créées, on affiche le formulaire groupé des réponses
	if empty_answer == True:
		#On créé un formulaire groupé de n questions du formulaire DynMCQanswerForm
		DynMCQanswerSet = formset_factory(DynMCQanswerForm, extra = int(nb_answers))
		
		#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
		data = {
			'form-TOTAL_FORMS': int(nb_answers),
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': '',
		}
	
		form = DynMCQanswerSet()
		if request.method == 'POST':
			form = DynMCQanswerSet(request.POST)
			if form.is_valid():
				answer_count = 1
				#Remplissage automatique des champs id_test et q_num
				for instance in form:
					dynMCQanswer = instance.save(commit=False)
					dynMCQanswer.id_test = input_id_test
					dynMCQanswer.q_num = input_q_num
					dynMCQanswer.ans_num = answer_count
					answer_count += 1
					dynMCQanswer.save()
					empty_answer = False
					#On récupère les réponses pour les afficher
					DynMCQanswerTest = DynMCQanswer.objects.filter(id_test = input_id_test, q_num = input_q_num)
					DynMCQanswerTest_List = []
					for instance in DynMCQanswerTest:
						DynMCQanswerTest_List.append(instance)
				form = DynMCQanswerSet()
			
	context = {
		'form' : form,
		'DynMCQquestionTest' : DynMCQquestionTest,
		'DynMCQTestInfo' : DynMCQTestInfo,
		'DynMCQanswerTest_List' : DynMCQanswerTest_List,
		'empty_answer' : empty_answer,
	}
	return render(request, 'manage_tests/test_create_dynmcqanswer.html',context)
	
def DynMCQTest_pass_menu_view(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	empty_passdynMCQtest = True
	
	Pass_DynMCQInfo = []
	#Formulaire du Pass_DynMCQTestInfoForm
	form = Pass_DynMCQTestInfoForm(request.POST or None)
	#Formulaire des infos du pass_dyntest
	if form.is_valid():
		passdynmcqtest = form.save(commit = False)
		passdynmcqtest.id_test = input_id_test
		passdynmcqtest.mark = 0
		input_id_student = passdynmcqtest.id_student
		passdynmcqtest.save()
		form = Pass_DynMCQTestInfoForm()
		empty_passdynMCQtest = False
		Pass_DynMCQInfo = get_object_or_404(Pass_DynMCQTest_Info, id_test=input_id_test, id_student = input_id_student)
			
	context = {
		'DynMCQTestInfo' : DynMCQTestInfo,
		'empty_passdynMCQtest' : empty_passdynMCQtest,
		'form': form,
		'Pass_DynMCQInfo' : Pass_DynMCQInfo,
	}
	return render(request, 'pass_tests/menu_pass_dynmcqtest.html',context)

def DynMCQtest_pass_view(request,input_id_test, input_id_student):
	#Récupération des informations du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	Pass_DynMCQInfo = get_object_or_404(Pass_DynMCQTest_Info, id_test=input_id_test, id_student = input_id_student)
	DynMCQquestions = DynMCQquestion.objects.filter(id_test = input_id_test)
	DynMCQanswers = DynMCQanswer.objects.filter(id_test = input_id_test)
	
	#On met les questions dans une liste
	DynMCQquestions_List = []
	for instance in DynMCQquestions:
		DynMCQquestions_List.append(instance)
		
	#On ordonne les questions et les réponses dans une même liste pour l'affichage
	Questions_Answers_List = []
	for question in DynMCQquestions:
		Questions_Answers_List.append(question)
		DynMCQanswers = DynMCQanswer.objects.filter(id_test = input_id_test, q_num = question.q_num)
		for answer in DynMCQanswers:
			Questions_Answers_List.append(answer)
	
	nb_questions = DynMCQTestInfo.nb_q
	#On créé un formulaire groupé de pass_dyntest du nombre de question du test
	PassDynMCQTestSet = formset_factory(Pass_DynMCQTestForm, extra = int(nb_questions))
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': int(nb_questions),
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	form_answers = PassDynMCQTestSet()
	if request.method == 'POST':
		form_answers = PassDynMCQTestSet(request.POST)
	
		if form_answers.is_valid():
			question_count = 1
			#Remplissage automatique des champs id_test et q_num
			for instance in form_answers:
				pass_dynMCQtest = instance.save(commit=False)
				pass_dynMCQtest.id_test = input_id_test
				pass_dynMCQtest.id_student = input_id_student
				pass_dynMCQtest.q_num = question_count
				#On récupère la réponse associé et on test si la réponse est bonne
				the_answer = get_object_or_404(DynMCQanswer, id_test=input_id_test, q_num = question_count, right_ans = 1)
				#Si la réponse est bonne, on incrémente la note du test
				if(int(pass_dynMCQtest.r_ans) == the_answer.ans_num):
					Pass_DynMCQInfo.mark += 1
					Pass_DynMCQInfo.save()
				question_count += 1
				pass_dynMCQtest.save()
			form_answers = PassDynMCQTestSet()
	context = {
		'Pass_DynMCQInfo' : Pass_DynMCQInfo,
		'DynMCQTestInfo':DynMCQTestInfo,
		'form_answers': form_answers,
		'DynMCQquestions_List' : DynMCQquestions_List,
		'Questions_Answers_List' : Questions_Answers_List,
	}
	return render(request, 'pass_tests/dynMCQtest_pass.html', context)
	
def pass_dynMCQtest_display_view(request,input_id_test,input_id_student):
	# Retrieve and display the requested mcq form
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	Pass_DynMCQInfo = get_object_or_404(Pass_DynMCQTest_Info, id_test=input_id_test, id_student = input_id_student)
	Pass_DynMCQtest = Pass_DynMCQTest.objects.filter(id_test = input_id_test, id_student = input_id_student)
	Pass_DynMCQtest_List = []
	for instance in Pass_DynMCQtest:
		Pass_DynMCQtest_List.append(instance)
	context = {
		'DynMCQTestInfo' : DynMCQTestInfo,
		'Pass_DynMCQInfo' : Pass_DynMCQInfo,
		'Pass_DynMCQtest_List': Pass_DynMCQtest_List,
	}
	return render(request, 'manage_tests/pass_dynMCQtest_display.html', context)
	
def Edit_DynMCQquestion_view(request,input_id_test,input_q_num):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = input_q_num)
	
	form = DynMCQquestionForm_question(request.POST, instance = DynMCQquestionTest)
	if form.is_valid():
		form.save()
		form = DynMCQquestionForm_question(instance = DynMCQquestionTest)
			
	context = {
		'DynMCQTestInfo':DynMCQTestInfo,
		'form': form,
		'DynMCQquestionTest':DynMCQquestionTest,
	}
	return render(request, 'manage_tests/edit_dynMCQquestion.html', context)
	
def Edit_DynMCQanswer_view(request,input_id_test,input_q_num,input_ans_num):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = input_q_num)
	DynMCQanswerTest = get_object_or_404(DynMCQanswer, id_test=input_id_test, q_num = input_q_num, ans_num = input_ans_num)
	
	form = DynMCQanswerForm(request.POST, instance = DynMCQanswerTest)
	if form.is_valid():
		form.save()
		form = DynMCQanswerForm(instance = DynMCQanswerTest)
			
	context = {
		'DynMCQTestInfo':DynMCQTestInfo,
		'form': form,
		'DynMCQquestionTest':DynMCQquestionTest,
		'DynMCQanswerTest' : DynMCQanswerTest,
	}
	return render(request, 'manage_tests/edit_dynMCQanswer.html', context)
	
def Delete_DynMCQquestion_view(request,input_id_test,input_q_num):
	#Récupération des informations du test et de la question à supprimer
	DynMCQTestInfo = get_object_or_404(DynMCQInfo,id_test = input_id_test)
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = input_q_num)
	
	#On récupère le nombre de question et le numéro de la question
	nb_questions = int(DynMCQTestInfo.nb_q)
	question_num = int(input_q_num) + 1
	
	#Suppression de la question
	DynMCQquestionTest.delete()
	
	#Modification du nombre de question du test
	tmp_nb_q = int(DynMCQTestInfo.nb_q) - 1
	DynMCQTestInfo.nb_q = str(tmp_nb_q)
	DynMCQTestInfo.save()
	
	#Récupération pui suppression des réponses liées à la question
	answers = DynMCQanswer.objects.filter(id_test = input_id_test, q_num = input_q_num)
	answers_list = []
	for instance in answers :
			answers_list.append(instance)
	for instance in answers_list :
		instance.delete()
	
	#On décale les numéros des questions et réponses des questions qui suivent la question supprimée
	while question_num <= nb_questions : 
		tmp_question = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = question_num)
		tmp_question.q_num -= 1
		tmp_question.save()
		
		the_answers = DynMCQanswer.objects.filter(id_test = input_id_test, q_num = question_num)
		the_answers_list = []
		for instance in the_answers :
			the_answers_list.append(instance)
		for instance in the_answers_list :
			instance.q_num -= 1
			instance.save()
		question_num += 1
			
	#Récupération des questions du test
	DynMCQquestionTest = DynMCQquestion.objects.filter(id_test=input_id_test)
	
	#On met les questions dans une liste
	DynMCQquestionTestList = []
	for instance in DynMCQquestionTest:
		DynMCQquestionTestList.append(instance)		
	
	context = {
		'DynMCQTestInfo':DynMCQTestInfo,
		'DynMCQquestionTestList': DynMCQquestionTestList,
	}
	return render(request, 'manage_tests/selectmenu_dynmcqtest.html', context)
	
def Delete_DynMCQanswer_view(request,input_id_test,input_q_num,input_ans_num):
	#Récupération des informations du test, question de la réponse et réponse à supprimer
	DynMCQTestInfo = get_object_or_404(DynMCQInfo,id_test = input_id_test)
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = input_q_num)
	DynMCQanswerTest = get_object_or_404(DynMCQanswer, id_test=input_id_test, q_num = input_q_num, ans_num = input_ans_num)
	
	#Récupération du nombre de réponses de la question
	nb_answers = int(DynMCQquestionTest.nb_ans)
	answer_num = int(input_ans_num) + 1
	
	#Suppression de la réponse
	DynMCQanswerTest.delete()
	#Modification du nombre de réponses
	tmp_nb_ans = int(DynMCQquestionTest.nb_ans) - 1
	DynMCQquestionTest.nb_ans = str(tmp_nb_ans)
	DynMCQquestionTest.save()
	
	#On décale les numéros des réponses suivant celle qu'on vient de supprimer
	while answer_num <= nb_answers : 
		tmp_answer = get_object_or_404(DynMCQanswer, id_test=input_id_test, q_num = input_q_num,ans_num = answer_num)
		tmp_answer.ans_num -= 1
		tmp_answer.save()
		answer_num += 1
	
	#Récupération de la liste de réponse
	the_DynMCQanswer = DynMCQanswer.objects.filter(id_test = input_id_test, q_num = input_q_num)
	DynMCQanswerTest_List = []
	for instance in the_DynMCQanswer :
		DynMCQanswerTest_List.append(instance)
	empty_question = False
	empty_answer = False
			
	context = {
		'DynMCQTestInfo':DynMCQTestInfo,
		'DynMCQquestionTest' : DynMCQquestionTest,
		'DynMCQanswerTest_List' : DynMCQanswerTest_List,
		'empty_question' : empty_question,
		'empty_answer' : empty_answer,
	}
	return render(request, 'manage_tests/test_create_dynmcqquestion.html', context)
	
def Add_DynMCQquestion_view(request, input_id_test):
	#Récupération des informations du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	
	#Récupération et modification du nombre de question
	nb_questions = int(DynMCQTestInfo.nb_q) + 1
	DynMCQTestInfo.nb_q = int(nb_questions)
	DynMCQTestInfo.save()
	
	#Création de la nouvelle question
	DynamicMCQquestion = DynMCQquestion(id_test = input_id_test, q_num = nb_questions)
	DynamicMCQquestion.save()
			
	#Récupération des questions du test
	DynMCQquestionTest = DynMCQquestion.objects.filter(id_test=input_id_test)
	
	#On met les questions dans une liste
	DynMCQquestionTestList = []
	for instance in DynMCQquestionTest:
		DynMCQquestionTestList.append(instance)
			
	context = {
		'DynMCQquestionTestList': DynMCQquestionTestList,
		'DynMCQTestInfo': DynMCQTestInfo,
	}
	return render(request, 'manage_tests/selectmenu_dynmcqtest.html',context)
	
def Add_DynMCQanswer_view(request,input_id_test,input_q_num):
	#Récupération des informations du test et de la question du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, id_test=input_id_test, q_num = input_q_num)
	
	add_answer = False
	
	#Récupération du nombre de réponses de la question
	nb_answers = int(DynMCQquestionTest.nb_ans) + 1
	
	#Formulaire de la nouvelle réponse
	form = DynMCQanswerForm(request.POST)
	if form.is_valid():
		the_answer = form.save(commit = False)
		the_answer.id_test = input_id_test
		the_answer.q_num = input_q_num
		the_answer.ans_num = nb_answers
		the_answer.save()
		#On modifie le nombre de réponses de la question
		DynMCQquestionTest.nb_ans = int(nb_answers)
		DynMCQquestionTest.save()
		add_answer = True
			
	context = {
		'add_answer':add_answer,
		'nb_answers' : nb_answers,
		'DynMCQTestInfo':DynMCQTestInfo,
		'form': form,
		'DynMCQquestionTest':DynMCQquestionTest,
	}
	return render(request, 'manage_tests/add_dynMCQanswer.html', context)
	
def DynTest_create_view(request,input_id_test):
	#Récupération des informations du test
	DynTestInforms = get_object_or_404(DynTestInfo, id_test=input_id_test)
	
	#DynTestListAll = DynTest.objects.all()
	#DynTestList = []
	#DynTestExist = False
	#for dyntest in DynTestListAll:
	#	if dyntest.id_test == DynTestInfo.id_test:
	#		DynTestExist = True
	#		DynTestList.append(dyntest)
			
	nb_questions = DynTestInforms.nb_q
	
	#On créé un formulaire groupé de n questions du formulaire DynTestForm
	DynTestSet = formset_factory(DynTestForm, extra = int(nb_questions))
		
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': int(nb_questions),
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	
	form = DynTestSet()
	if request.method == 'POST':
		form = DynTestSet(request.POST)
		if form.is_valid():
			question_count = 1
			#Remplissage automatique des champs id_test et q_num
			for instance in form:
				dyntest = instance.save(commit=False)
				dyntest.id_test = input_id_test
				dyntest.q_num = question_count
				question_count += 1
				dyntest.save()
			form = DynTestSet()
			
	context = {
		'form': form,
		'DynTestInforms': DynTestInforms,
	}
	return render(request, 'manage_tests/test_create_dyntest.html',context)
	
def DynTest_menu_view(request):
	#Formulaire du DynTestInfo
	form = DynTestInfoForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = DynTestInfoForm()
	
	#On teste s'il y a des question (DynTest) qui ont le même id_test que les DynTestInfo
	#pour vérifier si le questionnaire est rempli de questions ou non
	#S'il le questionnaire est vide, on l'affiche sur la page html.
	DynTestInfo_list_all = DynTestInfo.objects.all()
	DynTestInfo_list = []
	DynTest_list_all = DynTest.objects.all()
	for dyntestinfo in DynTestInfo_list_all:
		dyntestfull = False
		for dyntest in DynTest_list_all:
			if dyntestinfo.id_test == dyntest.id_test:
				dyntestfull = True
		if dyntestfull == False:
			DynTestInfo_list.append(dyntestinfo)
			
	context = {
		'form': form,
		'DynTestInfo_list' : DynTestInfo_list,
	}
	return render(request, 'manage_tests/menu_dyntest.html',context)
	
def test_mcqtest_create_view(request):
	""" Show page to create a standard test (inputting text as answers) """
	form = MCQTestForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = MCQTestForm()

	context = {
		'form': form
	}
	return render(request, 'manage_tests/test_create_mcqtest.html', context)


def test_mcq_create_view(request):
	""" Show page to create a mcq test (selecting a choice among others) """
	form = TestMcqForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = TestMcqForm()

	context = {
		'form': form
	}
	return render(request, 'manage_tests/test_create_mcq.html', context)
	
def test_mcqtest_display_view(request, input_id_test):
	""" Show page displaying a given test questions """
	# Retrieve and display the requested form
	form = get_object_or_404(MCQTest, id_test=input_id_test)
	context = {
		'form': form
	}
	return render(request, 'manage_tests/test_mcqtest_display.html', context)


def test_display_view(request, input_id_test):
	""" Show page displaying a given test questions """
	# Retrieve and display the requested form
	form = get_object_or_404(Test_end_session, id_test=input_id_test)
	context = {
		'form': form
	}
	return render(request, 'manage_tests/test_display.html', context)


def test_pass_view(request, input_id_test):
	form_questions = get_object_or_404(Test_end_session, id_test=input_id_test)
	form_answers = PassTestForm(request.POST or None)
	#form_answers.id_student = ?

	if form_answers.is_valid():
		form_answers.save()

		# # Assess grade:
		# assessment = form_answers.assess_answer()

		# if not assessment['comment'] == 'pass':
		# 	# TODO: display indication to retry
		# 	form_answers = PassTestForm()
		# else:
		# 	# TODO: display indication that test is passed
		# 	form_answers = PassTestForm()

		form_answers = PassTestForm()

	context = {
		'form_answers': form_answers,
		'form_questions': form_questions
	}
	return render(request, 'pass_tests/test_pass.html', context)
	
def test_mcqtest_pass_view(request, input_id_test):
	form_questions = get_object_or_404(MCQTest, id_test=input_id_test)
	form_answers = PassMCQTestForm(request.POST or None,initial={'id_MCQTest': input_id_test})

	if form_answers.is_valid():
		form_answers.save()
		form_answers = PassMCQTestForm()

	context = {
		'form_answers': form_answers,
		'form_questions': form_questions
	}
	return render(request, 'pass_tests/test_mcqtest_pass.html', context)


def test_mcq_pass_view(request, input_id_test):
	form_questions = get_object_or_404(Test_mcq_end_session, id_test=input_id_test)
	form_answers = PassTestMcqForm(request.POST or None)
	#form_answers.id_student = ?

	if form_answers.is_valid():
		form_answers.save()

		# # Assess grade:
		# assessment = form_answers.assess_answer()

		# if not assessment['comment'] == 'pass':
		# 	# TODO: display indication to retry
		# 	form_answers = PassTestMcqForm()
		# else:
		# 	# TODO: display indication that test is passed
		# 	form_answers = PassTestMcqForm()

		form_answers = PassTestMcqForm()

	context = {
		'form_answers': form_answers,
		'form_questions': form_questions
	}
	return render(request, 'pass_tests/test_mcq_pass.html', context)
	
def dyntest_pass_view(request, input_id_test):
	DynTestInforms = get_object_or_404(DynTestInfo, id_test=input_id_test)
	testlist_dyntest_all = DynTest.objects.all()
	form_questions = []
	#On récupère les dynamics test
	for dyntest in testlist_dyntest_all:
		if dyntest.id_test == input_id_test:
			form_questions.append(dyntest)
	
	nb_questions = DynTestInforms.nb_q
	#On créé un formulaire groupé de pass_dyntest du nombre de question du test
	PassDynTestSet = formset_factory(Pass_DynTestForm, extra = int(nb_questions))
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': int(nb_questions),
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	form_answers = PassDynTestSet()
	if request.method == 'POST':
		form_answers = PassDynTestSet(request.POST)
	
		if form_answers.is_valid():
			question_count = 1
			#Remplissage automatique des champs id_test et q_num
			for instance in form_answers:
				pass_dyntest = instance.save(commit=False)
				pass_dyntest.id_test = input_id_test
				pass_dyntest.q_num = question_count
				question_count += 1
				pass_dyntest.save()
			form_answers = PassDynTestSet()
	context = {
		'DynTestInforms':DynTestInforms,
		'form_answers': form_answers,
		'form_questions': form_questions,
	}
	return render(request, 'pass_tests/dyntest_pass.html', context)
	
def pass_testslist_teacher_view(request):
	# List all the pass tests of the db
	pass_tests_list_normal_questions = Pass_test_end_session.objects.all()
	pass_testlist_mcqtest = Pass_MCQTest_end_session.objects.all()
	pass_dyntest_all = Pass_DynTest.objects.all()
	pass_dyntest_list = []
	id_student_list = []
	for dyntest in pass_dyntest_all:
		if dyntest.id_student not in id_student_list:
			pass_dyntest_list.append(dyntest)
			id_student_list.append(dyntest.id_student)
	pass_dynMCQtest_all = Pass_DynMCQTest_Info.objects.all()
	
	context = {
		'pass_tests_list': pass_tests_list_normal_questions,
		'pass_tests_mcqtest_list': pass_testlist_mcqtest,
		'pass_dyntest_list': pass_dyntest_list,
		'pass_dynMCQtest_all': pass_dynMCQtest_all,
	}
	return render(request, 'manage_tests/pass_tests_list_teacher.html', context)



def tests_list_teacher_view(request):
	# List all the tests of the db
	tests_list_normal_questions = Test_end_session.objects.all()
	testlist_mcq = Test_mcq_end_session.objects.all()
	testlist_mcqtest = MCQTest.objects.all()
	testlist_dyntestinfo_all = DynTestInfo.objects.all()

	context = {
		'tests_list': tests_list_normal_questions,
		'tests_mcq_list': testlist_mcq,
		'tests_mcqtest_list': testlist_mcqtest,
		'testlist_dyntestinfo_all':testlist_dyntestinfo_all,
	}
	return render(request, 'manage_tests/tests_list_teacher.html', context)

def tests_list_student_view(request):
	# List all the tests of the db
	tests_list_normal_questions = Test_end_session.objects.all()
	testlist_mcq = Test_mcq_end_session.objects.all()
	testlist_mcqtest = MCQTest.objects.all()
	testlist_dyntestinfo_all = DynTestInfo.objects.all()
	testlist_dynmcqtestinfo_all = DynMCQInfo.objects.all()

	context = {
		'tests_list': tests_list_normal_questions,
		'tests_mcq_list': testlist_mcq,
		'tests_mcqtest_list': testlist_mcqtest,
		'testlist_dyntestinfo_all':testlist_dyntestinfo_all,
		'testlist_dynmcqtestinfo_all' : testlist_dynmcqtestinfo_all,
	}
	return render(request, 'pass_tests/tests_list_student.html', context)


def tests_history_view(request):
	# Show the history of results
	queryset = Pass_test_end_session.objects.all() #TODO: transform query to get id_student only
	context = {
		'tests_list': queryset
	}
	return render(request, 'pass_tests/tests_history.html', context)

def tests_analysis_view(request):
	# Analysis of the students' results
	queryset = Pass_test_end_session.objects.all()
	context = {
		'tests_list': queryset
	}
	return render(request, 'manage_tests/tests_analysis.html', context)


def test_mcq_display_view(request, input_id_test):
	# Retrieve and display the requested mcq form
	form = get_object_or_404(Test_mcq_end_session, id_test=input_id_test)
	context = {
		'form': form
	}
	return render(request, 'manage_tests/test_mcq_display.html', context)
	
def dyntest_display_view(request, input_id_test):
	dyntestinfo = get_object_or_404(DynTestInfo, id_test=input_id_test)
	testlist_dyntest_all = DynTest.objects.all()
	testlist_dyntest = []
	for dyntest in testlist_dyntest_all:
		if dyntest.id_test == input_id_test:
			testlist_dyntest.append(dyntest)
	context = {
		'dyntestinfo':dyntestinfo,
		'testlist_dyntest': testlist_dyntest,
	}
	return render(request, 'manage_tests/dyntest_display.html', context)
	
def pass_test_display_view(request, input_id_test):
	# Retrieve and display the requested mcq form
	form = get_object_or_404(Pass_test_end_session, id_test=input_id_test)
	context = {
		'form': form
	}
	return render(request, 'manage_tests/pass_test_display.html', context)
	
def pass_mcqtest_display_view(request, input_id_test):
	# Retrieve and display the requested mcq form
	form = get_object_or_404(Pass_MCQTest_end_session, id_test=input_id_test)
	context = {
		'form': form
	}
	return render(request, 'manage_tests/pass_mcqtest_display.html', context)
	
def pass_dyntest_display_view(request, input_id_student):
	# Retrieve and display the requested mcq form
	pass_dyntest_all = Pass_DynTest.objects.all()
	pass_dyntest_list = []
	for dyntest in pass_dyntest_all:
		if dyntest.id_student == input_id_student:
			pass_dyntest_list.append(dyntest)
	context = {
		'pass_dyntest_list': pass_dyntest_list
	}
	return render(request, 'manage_tests/pass_dyntest_display.html', context)
	
def dashboard_view(request):
	testlist_mcqtest = MCQTest.objects.all()
	context = {
		'tests_mcqtest_list': testlist_mcqtest
	}
	return render(request, 'manage_tests/dashboard.html', context)
	
	
def statistics_view(request, input_id_test):
	mcqtest = get_object_or_404(MCQTest, id_test=input_id_test)
	pass_mcqtest_list_all = Pass_MCQTest_end_session.objects.all()
	pass_mcqtest_list = []
	
	#On récupère les pass_tests liés au MCQTest
	#Pour cela on ajoute ceux dont l'id_MCQTest est le même que celui du MCQTest
	i = 0
	while i < len(pass_mcqtest_list_all):
		if pass_mcqtest_list_all[i].id_MCQTest == input_id_test:
			pass_mcqtest_list.append(pass_mcqtest_list_all[i])
		i += 1
	
	statistiques_notes = [0,0,0,0,0,0]
	
	#On calcul les notes aux pass_test liés aux MCQTest
	marks_list=[]
	i = 0
	while i < len(pass_mcqtest_list):
		note = 0
		if pass_mcqtest_list[i].q1 == mcqtest.r1:
			note += 1
		if pass_mcqtest_list[i].q2 == mcqtest.r2:
			note += 1
		if pass_mcqtest_list[i].q3 == mcqtest.r3:
			note += 1
		if pass_mcqtest_list[i].q4 == mcqtest.r4:
			note += 1
		if pass_mcqtest_list[i].q5 == mcqtest.r5:
			note += 1
		pass_mcqtest_list[i].mark = note
		pass_mcqtest_list[i].save()
		marks_list.append(pass_mcqtest_list[i].mark)
		statistiques_notes[note] += 1
		i += 1
		
	#Calcul de la moyenne et des notes hautes et basses
	moyenne_mcqtest = 0
	note_plus_basse = 5
	note_plus_haute = 0
	i = 0
	while i < len(pass_mcqtest_list):
		moyenne_mcqtest += pass_mcqtest_list[i].mark
		if pass_mcqtest_list[i].mark < note_plus_basse:
			note_plus_basse = pass_mcqtest_list[i].mark
		if pass_mcqtest_list[i].mark > note_plus_haute:
			note_plus_haute = pass_mcqtest_list[i].mark
		i += 1
	moyenne_mcqtest /= len(pass_mcqtest_list)
	moyenne_mcqtest="%.2f" % moyenne_mcqtest
	nb_test = len(pass_mcqtest_list)
	
	#Calcul du 1er et du 3eme quartile du test
	marks_list.sort()
	if len(marks_list)%4 == 0:
		q1=marks_list[len(marks_list)//4-1]
		q3=marks_list[3*len(marks_list)//4-1]
	else:
		q1=marks_list[len(marks_list)//4]
		q3=marks_list[3*len(marks_list)//4]

    #Calcul de la mediane
	marks_list.sort()
	if len(marks_list)%2 == 0:
		m=((marks_list[(len(marks_list)-1)//2]+marks_list[len(marks_list)//2])/2)
	else:
		m = marks_list[len(marks_list)//2]
		
	#Calcul des fréquences
	total_freq = []
	somme_freq = 0
	i = 0
	while i < len(statistiques_notes):
		temp_freq = 100 * statistiques_notes[i] / len(pass_mcqtest_list)
		somme_freq += temp_freq
		temp_freq = "%.2f" % temp_freq
		som_freq = "%.2f" % somme_freq
		total_freq.append((temp_freq,som_freq))
		i += 1
	
	#On met dans une liste les statistiques liés à chaque question
	stats_question = [0,0,0,0,0]
	i = 0
	while i < len(pass_mcqtest_list):
		if pass_mcqtest_list[i].q1 == mcqtest.r1:
			stats_question[0] += 1
		if pass_mcqtest_list[i].q2 == mcqtest.r2:
			stats_question[1] += 1
		if pass_mcqtest_list[i].q3 == mcqtest.r3:
			stats_question[2] += 1
		if pass_mcqtest_list[i].q4 == mcqtest.r4:
			stats_question[3] += 1
		if pass_mcqtest_list[i].q5 == mcqtest.r5:
			stats_question[4] += 1
		i += 1
		
	#Pourcentage des statistiques par question
	pourcentage_question = []
	i = 0
	while i < len(stats_question):
		pourcentage = 100*stats_question[i]/len(pass_mcqtest_list)
		pourcentage = "%.2f" % pourcentage
		pourcentage_question.append(pourcentage)
		i += 1
		
	total_statistics_question = []
	i = 0
	while i < len(stats_question):
		total_statistics_question.append((stats_question[i],pourcentage_question[i]))
		i += 1
	
	#Création des graphs
	GraphsQuestions(stats_question,pass_mcqtest_list)
	GraphsNote(total_freq)
	GraphsBoxplot(marks_list)

	context = {
		'mcqtest': mcqtest,
		'pass_mcqtest_list': pass_mcqtest_list,
		'moyenne_mcqtest' : moyenne_mcqtest,
		'nb_test' : nb_test,
		'note_plus_haute' : note_plus_haute,
		'note_plus_basse' : note_plus_basse,
		'q1' : q1,
		'q3' : q3,
		'mediane' : m,
		'total_statistics_question' : total_statistics_question,
		'total_freq' : total_freq,
	}
	return render(request, 'manage_tests/statistics.html', context)
	
#Graphique statistiques par question
def GraphsQuestions(stats_question,pass_mcqtest_list):
	plt.rcdefaults()
	fig, ax = plt.subplots()

	questions = ('q1', 'q2', 'q3', 'q4', 'q5')
	y_pos = np.arange(len(stats_question))
	performance = stats_question

	ax.barh(y_pos, performance, align='center')
	ax.set_yticks(y_pos)
	ax.set_yticklabels(questions)
	ax.invert_yaxis()
	ax.set_xlabel('Bonnes réponses')
	ax.set_title('Stats Questions')
	plt.savefig('./pages/static/images/GraphsQuestions.png')
	
#Graphique statistiques des notes
def GraphsNote(total_freq):
	labels = '0/5', '1/5', '2/5', '3/5', '4/5', '5/5'
	sizes = []
	for q in total_freq:
		sizes.append(q[0])
	fig, ax = plt.subplots()
	ax.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
	ax.axis('equal')
	ax.set_title('Statistiques des notes')
	plt.savefig('./pages/static/images/GraphsNote.png')
	
#Boxplot du test
def GraphsBoxplot(marks_list):
	data = marks_list
	fig, ax = plt.subplots()
	ax.boxplot(data,vert=False,)
	ax.set_title('Boxplot du test')
	plt.savefig('./pages/static/images/GraphsBoxplot.png')
	



