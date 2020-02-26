from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory
from .forms import TestForm, PassTestForm, TestMcqForm, PassTestMcqForm, MCQTestForm, PassMCQTestForm, DynTestForm, Pass_DynTestForm,DynTestInfoForm,DynMCQTestInfoForm,DynMCQquestionForm,DynMCQanswerForm,Pass_DynMCQTestForm,DynMCQquestionForm_question,Pass_DynMCQTestInfoForm,DynMCQTestInfoForm,DynMCQTestInfoForm_questions,Question_difficulty_form,MCQQuestion_difficulty_form,DynMCQTestInfoForm_launch,DynquestionForm
from .models import Test_end_session, Pass_test_end_session, Test_mcq_end_session, MCQTest, Pass_MCQTest_end_session, DynTest,Pass_DynTest,DynTestInfo,DynMCQInfo,DynMCQquestion,DynMCQanswer,Pass_DynMCQTest,Pass_DynMCQTest_Info,Dynquestion
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time as tm
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,Group,Permission
from django.urls import reverse

def register_view(request):
	if request.method == 'POST':
		#Récupération des champs de l'utilisateur
		last_name = request.POST['last_name']
		first_name = request.POST['first_name']
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		function = request.POST['function']
		group1 = request.POST['group1']
		group2 = request.POST['group2']
		
		#Si l'utilisateur est déjà pris, on affiche un message d'erreur et on réaffiche la page
		if User.objects.filter(username=username).exists():
			messages.info(request,'Username taken')
			return redirect('tests:register')
		#Même principe pour l'email
		elif User.objects.filter(email=email).exists():
			messages.info(request,'Email already used')
			return redirect('tests:register')
		#Vérification que l'utilisateur écrit bien Teacher ou Student
		elif function != "Teacher" and function != "Student":
			messages.info(request,'Function not correct')
			return redirect('tests:register')
		#Création de l'utilisateur
		else:
			user = User.objects.create_user(username=username,password=password,last_name=last_name,first_name=first_name,email=email)
			#On associe le bon Groupe de Permissions à l'utilisateur
			if function == "Student":
				student = Group.objects.get(name='Student')
				user.groups.add(student)
			else:
				teacher = Group.objects.get(name='Teacher')
				user.groups.add(teacher)
			#Groupe de classe de l'élève
			group_1 = Group.objects.get(name=group1)
			user.groups.add(group_1)
			if group2 != "None":
				group_2 = Group.objects.get(name=group2)
				user.groups.add(group_2)
			
			#On enregistre l'utilisateur dans la base de donnée et on renvoie à la page d'accueil
			user.save()
			return redirect('/')
	else:
		return render(request,'register.html')

def login_view(request):
	if request.method == 'POST':
		#Récupération des champs d'authentification
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		#Si l'utilisateur existe, on authentifie et on renvoie à la page d'accueil
		if user is not None:
			login(request,user)
			return redirect('/')
		#Sinon on affiche un message d'erreur et on réaffiche la page
		else:
			messages.info(request,'Invalid user')
			return redirect('tests:login')
	else:
		return render(request,'login.html')
		
def logout_view(request):
	logout(request)
	return redirect('/')

# Create your views here.
@login_required
@permission_required('tests.can_create_test', raise_exception=True)
def test_create_view(request, *args, **kwargs):
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
		'testlist_dynmcqtestinfo_all':testlist_dynmcqtestinfo_all,
	}
	return render(request, 'manage_tests/test_create.html', context)


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
	
def Manage_questions_view(request):
	#Récupération des tests
	DynMCQquestions = DynMCQquestion.objects.all()
	Dynquestions = Dynquestion.objects.all()
			
	context = {
		'DynMCQquestions' : DynMCQquestions,
		'Dynquestions' : Dynquestions,
	}
	return render(request, 'manage_tests/manage_questions.html',context)
	
def DynMCQquestion_select_menu_view(request, input_id_test):
	#Récupération des informations du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	empty = False
	DynMCQquestionTestList = []
	DynquestionTestList = []
	#Récupération des questions du test
	if(DynMCQTestInfo.questions != ""):
		num_questions = get_questions(DynMCQTestInfo.questions)

		#On met les questions dans une listes
		mcq_questions = num_questions[0]
		normal_questions = num_questions[1]
		for i in range(len(mcq_questions)):
			DynMCQQuestion = DynMCQquestion.objects.get(q_num = mcq_questions[i])
			DynMCQquestionTestList.append(DynMCQQuestion)
		for i in range(len(normal_questions)):
			DynQuestion = Dynquestion.objects.get(q_num = normal_questions[i])
			DynquestionTestList.append(DynQuestion)

	form = []
	#S'il n'y a pas encore de questions créées, on créé autant de questions que précisé dans les informations du test
	if len(DynMCQquestionTestList) == 0 and len(DynquestionTestList) == 0:
		empty = True
		QuestionsSet = formset_factory(DynMCQTestInfoForm_questions, extra = 2)
		#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
		data = {
			'form-TOTAL_FORMS': 2,
			'form-INITIAL_FORMS': '0',
			'form-MAX_NUM_FORMS': '',
		}
	
		form = QuestionsSet()
		choices = []
		choices2 = []
		DynMCQquestions = DynMCQquestion.objects.all()
		Dynquestions = Dynquestion.objects.all()
		for question in DynMCQquestions:
			list = []
			list.append(int(question.q_num))
			list.append(question.q_text)
			choices.append(list)
		form[0].fields['questions'].choices = choices
		for question in Dynquestions:
			list = []
			list.append(int(question.q_num))
			list.append(question.q_text)
			choices2.append(list)
		form[1].fields['questions'].choices = choices2
		if request.method == 'POST':
			form = QuestionsSet(request.POST)
			choices = []
			choices2 = []
			DynMCQquestions = DynMCQquestion.objects.all()
			Dynquestions = Dynquestion.objects.all()
			for question in DynMCQquestions:
				list = []
				list.append(int(question.q_num))
				list.append(question.q_text)
				choices.append(list)
			form[0].fields['questions'].choices = choices
			for question in Dynquestions:
				list = []
				list.append(int(question.q_num))
				list.append(question.q_text)
				choices2.append(list)
			form[1].fields['questions'].choices = choices2
		
			if form.is_valid():
				test = form[0].save(commit = False)
				test2 = form[1].save(commit = False)
				DynMCQTestInfo.questions = "a" + test.questions + "b" + test2.questions
				DynMCQTestInfo.save()
				
				empty = False
				num_questions = get_questions(DynMCQTestInfo.questions)

				#On met les questions dans une liste
				mcq_questions = num_questions[0]
				normal_questions = num_questions[1]
				for i in range(len(mcq_questions)):
					DynMCQQuestion = DynMCQquestion.objects.get(q_num = mcq_questions[i])
					DynMCQquestionTestList.append(DynMCQQuestion)
				for i in range(len(normal_questions)):
					DynQuestion = Dynquestion.objects.get(q_num = normal_questions[i])
					DynquestionTestList.append(DynQuestion)
			
	context = {
		'DynMCQquestionTestList': DynMCQquestionTestList,
		'DynquestionTestList': DynquestionTestList,
		'DynMCQTestInfo': DynMCQTestInfo,
		'form': form,
		'empty':empty,
	}
	return render(request, 'manage_tests/selectmenu_dynmcqtest.html',context)
	
def Question_reallocation_view(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	
	num_questions = get_questions(DynMCQTestInfo.questions)
	empty = True
	
	#On met les questions dans une liste
	DynMCQquestionTestList = []
	DynquestionTestList = []
	
	mcq_questions = num_questions[0]
	normal_questions = num_questions[1]
	for i in range(len(mcq_questions)):
		DynMCQQuestion = DynMCQquestion.objects.get(q_num = mcq_questions[i])
		DynMCQquestionTestList.append(DynMCQQuestion)
	for i in range(len(normal_questions)):
		DynQuestion = Dynquestion.objects.get(q_num = normal_questions[i])
		DynquestionTestList.append(DynQuestion)
				
	QuestionsSet = formset_factory(DynMCQTestInfoForm_questions, extra = 2)
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': 2,
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	
	form = QuestionsSet()
	choices = []
	choices2 = []
	DynMCQquestions = DynMCQquestion.objects.all()
	Dynquestions = Dynquestion.objects.all()
	for question in DynMCQquestions:
		list = []
		list.append(int(question.q_num))
		list.append(question.q_text)
		choices.append(list)
	form[0].fields['questions'].choices = choices
	for question in Dynquestions:
		list = []
		list.append(int(question.q_num))
		list.append(question.q_text)
		choices2.append(list)
	form[1].fields['questions'].choices = choices2
	if request.method == 'POST':
		form = QuestionsSet(request.POST)
		choices = []
		choices2 = []
		DynMCQquestions = DynMCQquestion.objects.all()
		Dynquestions = Dynquestion.objects.all()
		for question in DynMCQquestions:
			list = []
			list.append(int(question.q_num))
			list.append(question.q_text)
			choices.append(list)
		form[0].fields['questions'].choices = choices
		for question in Dynquestions:
			list = []
			list.append(int(question.q_num))
			list.append(question.q_text)
			choices2.append(list)
		form[1].fields['questions'].choices = choices2
		
		if form.is_valid():
			test = form[0].save(commit = False)
			test2 = form[1].save(commit = False)
			DynMCQTestInfo.questions = "a" + test.questions + "b" + test2.questions
			DynMCQTestInfo.save()
			
			empty = False
			num_questions = get_questions(DynMCQTestInfo.questions)

			#On met les questions dans une liste
			mcq_questions = num_questions[0]
			normal_questions = num_questions[1]
			DynMCQquestionTestList = []
			DynquestionTestList = []
			for i in range(len(mcq_questions)):
				DynMCQQuestion = DynMCQquestion.objects.get(q_num = mcq_questions[i])
				DynMCQquestionTestList.append(DynMCQQuestion)
			for i in range(len(normal_questions)):
				DynQuestion = Dynquestion.objects.get(q_num = normal_questions[i])
				DynquestionTestList.append(DynQuestion)
			
	context = {
		'DynMCQquestionTestList': DynMCQquestionTestList,
		'DynquestionTestList': DynquestionTestList,
		'DynMCQTestInfo': DynMCQTestInfo,
		'form': form,
		'empty':empty,
	}
	return render(request, 'manage_tests/question_reallocation.html',context)

def get_questions(questions):
	num_questions = []
	if "]b[" in questions:
		num_questions = questions.split("]b[")
		num_questions[0] = num_questions[0].replace("a","")
		num_questions[1] = num_questions[1].replace("b","")
		num_questions[0] = num_questions[0].replace("[","")
		num_questions[1] = num_questions[1].replace("]","")
		num_questions[0] = num_questions[0].replace("'","")
		num_questions[1] = num_questions[1].replace("'","")
		num_questions[0] = num_questions[0].split(",")
		num_questions[1] = num_questions[1].split(",")
	else:
		posA = questions.find("a")
		str = questions
		str = str.replace("a","")
		str = str.replace("b","")
		str = str.replace("[","")
		str = str.replace("]","")
		str = str.replace("'","")
		listquestions = str.split(",")
		list = []
		if(questions[posA+1] == "b"):
			num_questions.append(list)
			num_questions.append(listquestions)
		else :
			num_questions.append(listquestions)
			num_questions.append(list)
	return num_questions	
	
def DynMCQquestion_create_view(request, input_q_num):
	#Récupération la question sélectionnée du test
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, q_num = input_q_num)
	#On récupère les réponses liées à la question
	DynMCQanswerTest = DynMCQanswer.objects.filter(q_num = input_q_num)
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
	}
	return render(request, 'manage_tests/test_create_dynmcqquestion.html',context)
	
def Dynquestion_create_view(request, input_q_num):
	#Récupération la question sélectionnée du test
	DynquestionTest = get_object_or_404(Dynquestion, q_num = input_q_num)
	#On récupère les réponses liées à la question
	empty_question = True
	form = 0
	#Si la question n'a pas encore été "remplie", on affiche le formulaire de la question 
	if DynquestionTest.q_text == "":
		form = DynquestionForm(request.POST, instance = DynquestionTest)
		if form.is_valid():
			form.save()
			form = DynquestionForm()
			empty_question = False
	#Si la question a été rempli, on teste s'il y a des réponses déjà remplies pour les afficher 
	else:
		empty_question = False
			
			
	context = {
		'form': form,
		'empty_question': empty_question,
		'DynquestionTest' : DynquestionTest,
	}
	return render(request, 'manage_tests/test_create_dynquestion.html',context)
	
def Add_difficulty_view(request,input_q_num):
	#Récupération la question sélectionnée du test
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, q_num = input_q_num)
	empty = True
	DifficultySet = formset_factory(MCQQuestion_difficulty_form, extra = 5)
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': 5,
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	
	form = DifficultySet()

	for theme in form:
		choices = []
		for i in range(5):
			list = []
			list.append(i)
			list.append(i)
			choices.append(list)
		theme.fields['difficulty'].choices = choices #Assignation des choix
		
	if request.method == 'POST':
		form = DifficultySet(request.POST)
		
		for theme in form:
			choices = []
			for i in range(5):
				list = []
				list.append(i)
				list.append(i)
				choices.append(list)
			theme.fields['difficulty'].choices = choices #Assignation des choix
	
		if form.is_valid():
			the_difficulty = ""
			for theme in form:
				the_theme = theme.save(commit=False)
				the_difficulty += the_theme.difficulty
			DynMCQquestionTest.difficulty = the_difficulty
			DynMCQquestionTest.save()
			empty = False
			
	context = {
		'form' : form,
		'DynMCQquestionTest' : DynMCQquestionTest,
		'empty' : empty,
	}
	return render(request, 'manage_tests/mcqquestion_difficulty.html',context)
	
def Add_difficulty_question_view(request,input_q_num):
	#Récupération la question sélectionnée du test
	DynquestionTest = get_object_or_404(Dynquestion, q_num = input_q_num)
	empty = True
	DifficultySet = formset_factory(Question_difficulty_form, extra = 5)
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': 5,
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	
	form = DifficultySet()

	for theme in form:
		choices = []
		for i in range(5):
			list = []
			list.append(i)
			list.append(i)
			choices.append(list)
		theme.fields['difficulty'].choices = choices #Assignation des choix
		
	if request.method == 'POST':
		form = DifficultySet(request.POST)
		
		for theme in form:
			choices = []
			for i in range(5):
				list = []
				list.append(i)
				list.append(i)
				choices.append(list)
			theme.fields['difficulty'].choices = choices #Assignation des choix
	
		if form.is_valid():
			the_difficulty = ""
			for theme in form:
				the_theme = theme.save(commit=False)
				the_difficulty += the_theme.difficulty
			DynquestionTest.difficulty = the_difficulty
			DynquestionTest.save()
			empty = False
			
	context = {
		'form' : form,
		'DynquestionTest' : DynquestionTest,
		'empty' : empty,
	}
	return render(request, 'manage_tests/question_difficulty.html',context)
		
	
def DynMCQanswer_create_view(request, input_q_num):
	#Récupération la question sélectionnée du test
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, q_num = input_q_num)
	
	empty_answer = True
	#Récupération des réponses du test
	DynMCQanswerTest = DynMCQanswer.objects.filter(q_num = input_q_num)
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
					dynMCQanswer.q_num = input_q_num
					dynMCQanswer.ans_num = answer_count
					answer_count += 1
					dynMCQanswer.save()
					empty_answer = False
					#On récupère les réponses pour les afficher
					DynMCQanswerTest = DynMCQanswer.objects.filter(q_num = input_q_num)
					DynMCQanswerTest_List = []
					for instance in DynMCQanswerTest:
						DynMCQanswerTest_List.append(instance)
				form = DynMCQanswerSet()
			
	context = {
		'form' : form,
		'DynMCQquestionTest' : DynMCQquestionTest,
		'DynMCQanswerTest_List' : DynMCQanswerTest_List,
		'empty_answer' : empty_answer,
	}
	return render(request, 'manage_tests/test_create_dynmcqanswer.html',context)
	
def DynMCQTest_pass_menu_view(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	empty_passdynMCQtest = True
	#On récupère les tentatives
	Pass_DynMCQInfo_filter = Pass_DynMCQTest_Info.objects.filter(id_test=input_id_test,id_student=request.user.username)
	Pass_DynMCQInfo_List = []
	Pass_DynMCQInfo = []
	for instance in Pass_DynMCQInfo_filter:
		Pass_DynMCQInfo_List.append(instance)
	#On récupère le nombre de tentative de l'élève
	nb_pass_test = len(Pass_DynMCQInfo_List)
	
	#On teste si un test a déjà été créé
	if nb_pass_test > 0:
		#Si oui, on teste si le pass test a ses réponses remplies -> si l'élève a passé le test
		if Pass_DynMCQTest.objects.filter(id_test = input_id_test,id_student = request.user.username,attempt = nb_pass_test).exists():
			#Dans ce cas il faut créé un nouveau pass test en faisant une nouvelle tentative
			empty_passdynMCQtest = True
		else:
			#Sinon on réaffiche la même tentative jusqu'à ce que l'élève le passe
			Pass_DynMCQInfo = get_object_or_404(Pass_DynMCQTest_Info, id_test=input_id_test, id_student = request.user.username,attempt = nb_pass_test)
			empty_passdynMCQtest = False
	
	#On créé une nouvelle tentative de pass test
	if empty_passdynMCQtest:
		passdynmcqtest = Pass_DynMCQTest_Info(id_test=input_id_test,id_student=request.user.username,attempt = nb_pass_test+1,mark = 0)
		passdynmcqtest.save()
		empty_passdynMCQtest = False
		Pass_DynMCQInfo = get_object_or_404(Pass_DynMCQTest_Info, id_test=input_id_test, id_student = request.user.username,attempt = nb_pass_test+1)
			
	context = {
		'DynMCQTestInfo' : DynMCQTestInfo,
		'empty_passdynMCQtest' : empty_passdynMCQtest,
		'Pass_DynMCQInfo' : Pass_DynMCQInfo,
	}
	return render(request, 'pass_tests/menu_pass_dynmcqtest.html',context)

def DynMCQtest_pass_view(request,input_id_test, input_id_student, input_attempt):
	#Récupération des informations du test
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	Pass_DynMCQInfo = get_object_or_404(Pass_DynMCQTest_Info, id_test=input_id_test, id_student = input_id_student, attempt = input_attempt)
	num_questions = get_questions(DynMCQTestInfo.questions)
	
	#On ordonne les questions et les réponses dans une même liste pour l'affichage
	Questions_List = []
	for i in range(len(num_questions)):
			Questions_List.append(DynMCQquestion.objects.get(q_num = num_questions[i]))
	
	nb_questions = len(num_questions)
	#On créé un formulaire groupé de pass_dyntest du nombre de question du test
	PassDynMCQTestSet = formset_factory(Pass_DynMCQTestForm, extra = int(nb_questions))
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': int(nb_questions),
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	
	form_answers = PassDynMCQTestSet()
	#On récupère les réponses de chaque questions et on les place dans les choix de réponses de l'élève pour les checkbox
	i = 0
	for ans in form_answers:
		choices = []
		DynMCQanswers = DynMCQanswer.objects.filter(q_num = num_questions[i])
		#Récupération des réponses dans des sous-listes ('valeur retournée','texte affiché') pour chaque réponse possible
		for answer in DynMCQanswers:
			list = []
			list.append(answer.ans_num)
			list.append(answer.ans_text)
			choices.append(list)
		ans.fields['r_ans'].choices = choices #Assignation des choix
		i += 1
		
	if request.method == 'POST':
		form_answers = PassDynMCQTestSet(request.POST)
		i = 0
		for ans in form_answers:
			choices = []
			DynMCQanswers = DynMCQanswer.objects.filter(q_num = num_questions[i])
			for answer in DynMCQanswers:
				list = []
				list.append(answer.ans_num)
				list.append(answer.ans_text)
				choices.append(list)
			ans.fields['r_ans'].choices = choices
			i += 1
	
		if form_answers.is_valid():
			question_count = 0
			Pass_DynMCQInfo.time = datetime.datetime.today()
			#Remplissage automatique des champs du test
			for instance in form_answers:
				pass_dynMCQtest = instance.save(commit=False)
				pass_dynMCQtest.id_test = input_id_test
				pass_dynMCQtest.id_student = input_id_student
				pass_dynMCQtest.q_num = num_questions[question_count]
				pass_dynMCQtest.attempt = input_attempt
				#On récupère la réponse associé et on test si la réponse est bonne
				right_answers = DynMCQanswer.objects.filter(q_num = num_questions[question_count], right_ans = 1)
				num_right_answers = []
				for ans in right_answers:
					num_right_answers.append(ans.ans_num)
				#Si la réponse est bonne, on incrémente la note du test
				if check_answer(pass_dynMCQtest.r_ans,num_right_answers):
					Pass_DynMCQInfo.mark += 1
					Pass_DynMCQInfo.save()
				question_count += 1
				pass_dynMCQtest.save()
			return redirect('/')
			form_answers = PassDynMCQTestSet()
	context = {
		'Pass_DynMCQInfo' : Pass_DynMCQInfo,
		'DynMCQTestInfo':DynMCQTestInfo,
		'form_answers': form_answers,
		'Questions_List' : Questions_List,
	}
	return render(request, 'pass_tests/dynMCQtest_pass.html', context)

#Fonction qui vérifie qu'une réponse donnée est bonne ou non
#Elle compare la réponse de l'étudiant à la bonne réponse puis renvoie true ou false
def check_answer(stu_answer,num_right_answers):
	right_answer = True
	num_right_answers.sort()
	stu_num_answer = []
	#stu_answer est une chaine de caractères contenant les numéros de la réponse de l'élève
	#On extrait les numéros de la chaine de caractères dans une liste "stu_num_answer"
	i = 0
	while i < len(stu_answer):
		if stu_answer[i].isdigit():
			stu_num_answer.append(int(stu_answer[i]))
		i += 1	
	stu_num_answer.sort()
	#Si il n'y a pas le meme nombre de réponses dans les 2 listes alors la réponse de l'élève ne peut pas être bonne
	if(len(num_right_answers) != len(stu_num_answer)):
		right_answer = False
	else:
		#On compare les 2 listes de réponses
		i = 0
		while i < len(num_right_answers):
			if(num_right_answers[i] != stu_num_answer[i]):
				right_answer = False
			i += 1
	return right_answer
			
	
def pass_dynMCQtest_display_view(request,input_id_test,input_id_student,input_attempt):
	# Retrieve and display the requested mcq form
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	Pass_DynMCQInfo = get_object_or_404(Pass_DynMCQTest_Info, id_test=input_id_test, id_student = input_id_student,attempt = input_attempt)
	Pass_DynMCQtest = Pass_DynMCQTest.objects.filter(id_test = input_id_test, id_student = input_id_student,attempt = input_attempt)
	nb_questions = len(get_questions(DynMCQTestInfo.questions))
	Pass_DynMCQtest_List = []
	for instance in Pass_DynMCQtest:
		Pass_DynMCQtest_List.append(instance)
	context = {
		'DynMCQTestInfo' : DynMCQTestInfo,
		'Pass_DynMCQInfo' : Pass_DynMCQInfo,
		'Pass_DynMCQtest_List': Pass_DynMCQtest_List,
		'nb_questions':nb_questions,
	}
	return render(request, 'manage_tests/pass_dynMCQtest_display.html', context)
	
def DynMCQtest_display_view(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	num_questions = get_questions(DynMCQTestInfo.questions)
	mcq_questions = num_questions[0]
	normal_questions = num_questions[1]
	
	DynMCQquestions_List = []
	Dynquestions_List = []
		
	for i in range(len(normal_questions)):
		DynQuestion = Dynquestion.objects.get(q_num = normal_questions[i])
		Dynquestions_List.append(DynQuestion)
	
	for i in range(len(mcq_questions)):
		DynMCQQuestion = DynMCQquestion.objects.get(q_num = mcq_questions[i])
		DynMCQquestions_List.append(DynMCQQuestion)
		
	DynMCQanswers = []
	for i in range(len(num_questions)):
		theDynMCQanswers = DynMCQanswer.objects.filter(q_num = int(mcq_questions[i]))
		for ans in theDynMCQanswers:
			DynMCQanswers.append(ans)
		
	#On ordonne les questions et les réponses dans une même liste pour l'affichage
	Questions_Answers_List = []
	for question in DynMCQquestions_List:
		Questions_Answers_List.append(question)
		DynMCQanswers = DynMCQanswer.objects.filter(q_num = question.q_num)
		for answer in DynMCQanswers:
			Questions_Answers_List.append(answer)
			
	context = {
		'DynMCQquestions_List':DynMCQquestions_List,
		'DynMCQTestInfo':DynMCQTestInfo,
		'Questions_Answers_List': Questions_Answers_List,
		'Dynquestions_List':Dynquestions_List,
	}
	return render(request, 'manage_tests/dynmcqtest_display.html', context)
	
def Edit_DynMCQquestion_view(request,input_q_num):
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, q_num = input_q_num)
	
	form = DynMCQquestionForm_question(request.POST, instance = DynMCQquestionTest)
	if form.is_valid():
		form.save()
		form = DynMCQquestionForm_question(instance = DynMCQquestionTest)
			
	context = {
		'form': form,
		'DynMCQquestionTest':DynMCQquestionTest,
	}
	return render(request, 'manage_tests/edit_dynMCQquestion.html', context)
	
def Edit_Dynquestion_view(request,input_q_num):
	DynquestionTest = get_object_or_404(Dynquestion, q_num = input_q_num)
	
	form = DynquestionForm(request.POST, instance = DynquestionTest)
	if form.is_valid():
		form.save()
		form = DynquestionForm(instance = DynquestionTest)
			
	context = {
		'form': form,
		'DynquestionTest':DynquestionTest,
	}
	return render(request, 'manage_tests/edit_dynquestion.html', context)
	
def Edit_DynMCQanswer_view(request,input_q_num,input_ans_num):
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, q_num = input_q_num)
	DynMCQanswerTest = get_object_or_404(DynMCQanswer, q_num = input_q_num, ans_num = input_ans_num)
	
	form = DynMCQanswerForm(request.POST, instance = DynMCQanswerTest)
	if form.is_valid():
		form.save()
		form = DynMCQanswerForm(instance = DynMCQanswerTest)
			
	context = {
		'form': form,
		'DynMCQquestionTest':DynMCQquestionTest,
		'DynMCQanswerTest' : DynMCQanswerTest,
	}
	return render(request, 'manage_tests/edit_dynMCQanswer.html', context)
	
def Delete_DynMCQquestion_view(request,input_q_num):
	#Récupération des informations du test et de la question à supprimer
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, q_num = input_q_num)
	
	#Suppression de la question
	DynMCQquestionTest.delete()
	
	
	#Récupération puis suppression des réponses liées à la question
	answers = DynMCQanswer.objects.filter(q_num = input_q_num)
	answers_list = []
	for instance in answers :
			answers_list.append(instance)
	for instance in answers_list :
		instance.delete()
			
	#Récupération des questions du test
	DynMCQquestions = DynMCQquestion.objects.all()		
	Dynquestions = Dynquestion.objects.all()	
	
	context = {
		'Dynquestions': Dynquestions,
		'DynMCQquestions': DynMCQquestions,
	}
	return render(request, 'manage_tests/manage_questions.html', context)
	
def Delete_Dynquestion_view(request,input_q_num):
	#Récupération des informations du test et de la question à supprimer
	DynquestionTest = get_object_or_404(Dynquestion, q_num = input_q_num)
	
	#Suppression de la question
	DynquestionTest.delete()
			
	#Récupération des questions du test
	DynMCQquestions = DynMCQquestion.objects.all()
	Dynquestions = Dynquestion.objects.all()		
	
	context = {
		'DynMCQquestions': DynMCQquestions,
		'Dynquestions': Dynquestions,
	}
	return render(request, 'manage_tests/manage_questions.html', context)
	
def Delete_DynMCQanswer_view(request,input_q_num,input_ans_num):
	#Récupération des informations du test, question de la réponse et réponse à supprimer
	DynMCQquestionTest = get_object_or_404(DynMCQquestion,q_num = input_q_num)
	DynMCQanswerTest = get_object_or_404(DynMCQanswer,q_num = input_q_num, ans_num = input_ans_num)
	
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
		tmp_answer = get_object_or_404(DynMCQanswer,q_num = input_q_num,ans_num = answer_num)
		tmp_answer.ans_num -= 1
		tmp_answer.save()
		answer_num += 1
	
	#Récupération de la liste de réponse
	the_DynMCQanswer = DynMCQanswer.objects.filter(q_num = input_q_num)
	DynMCQanswerTest_List = []
	for instance in the_DynMCQanswer :
		DynMCQanswerTest_List.append(instance)
	empty_question = False
	empty_answer = False
			
	context = {
		'DynMCQquestionTest' : DynMCQquestionTest,
		'DynMCQanswerTest_List' : DynMCQanswerTest_List,
		'empty_question' : empty_question,
		'empty_answer' : empty_answer,
	}
	return render(request, 'manage_tests/test_create_dynmcqquestion.html', context)
	
def Add_DynMCQquestion_view(request):	
	#Création de la nouvelle question
	DynamicMCQquestion = DynMCQquestion.objects.create()
	DynamicMCQquestion.save()
	
	DynMCQquestions = DynMCQquestion.objects.all()
	Dynquestions = Dynquestion.objects.all()
	
	context = {
		'DynMCQquestions' : DynMCQquestions,
		'Dynquestions' : Dynquestions,
	}

	return render(request, 'manage_tests/manage_questions.html',context)
	
def Add_Dynquestion_view(request):
	#Création de la nouvelle question
	Dynamicquestion = Dynquestion.objects.create()
	Dynamicquestion.save()
	
	DynMCQquestions = DynMCQquestion.objects.all()
	Dynquestions = Dynquestion.objects.all()
	
	context = {
		'DynMCQquestions' : DynMCQquestions,
		'Dynquestions' : Dynquestions,
	}

	return render(request, 'manage_tests/manage_questions.html',context)
	
def Add_DynMCQanswer_view(request,input_q_num):
	#Récupération des informations de la question du test
	DynMCQquestionTest = get_object_or_404(DynMCQquestion, q_num = input_q_num)
	
	add_answer = False
	
	#Récupération du nombre de réponses de la question
	nb_answers = int(DynMCQquestionTest.nb_ans) + 1
	
	#Formulaire de la nouvelle réponse
	form = DynMCQanswerForm(request.POST)
	if form.is_valid():
		the_answer = form.save(commit = False)
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
	DynTestInforms.print_test = True
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

@login_required
@permission_required('tests.can_see_test', raise_exception=True)
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

@login_required
@permission_required('tests.can_see_test', raise_exception=True)
def tests_list_teacher_view(request):
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
		'testlist_dynmcqtestinfo_all':testlist_dynmcqtestinfo_all,
	}
	return render(request, 'manage_tests/tests_list_teacher.html', context)

@login_required
@permission_required('tests.can_pass_test', raise_exception=True)
def tests_list_student_view(request):
	# List all the tests of the db
	tests_list_normal_questions = Test_end_session.objects.all()
	testlist_mcq = Test_mcq_end_session.objects.all()
	testlist_mcqtest = MCQTest.objects.all()
	testlist_dyntestinfo_all = DynTestInfo.objects.all()
	testlist_dynmcqtestinfo_all = DynMCQInfo.objects.all()
	testlist_dynmcqtestinfo_user = []
	
	user_groups = request.user.groups.all()
	test_groups = ""
	for test in testlist_dynmcqtestinfo_all:
		test_groups = test.activated_for
		test_groups = test_groups.replace("'","")
		test_groups = test_groups.replace("[","")
		test_groups = test_groups.replace("]","")
		test_groups = test_groups.split(',')
		for test_group in test_groups:
			for user_group in user_groups:
				if(str(test_group) == str(user_group)):
					testlist_dynmcqtestinfo_user.append(test)

	context = {
		'tests_list': tests_list_normal_questions,
		'tests_mcq_list': testlist_mcq,
		'tests_mcqtest_list': testlist_mcqtest,
		'testlist_dyntestinfo_all':testlist_dyntestinfo_all,
		'testlist_dynmcqtestinfo_user' : testlist_dynmcqtestinfo_user,
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

@login_required
@permission_required('tests.can_see_stats', raise_exception=True)
def dashboard_view(request):
	testlist_dynmcqtest = DynMCQInfo.objects.all()
	context = {
		'testlist_dynmcqtest': testlist_dynmcqtest
	}
	return render(request, 'manage_tests/dashboard.html', context)
	
@login_required
@permission_required('tests.can_see_test', raise_exception=True)
def launch_view(request):
	testlist_dyntest = DynTestInfo.objects.all()
	testlist_dynmcqtest = DynMCQInfo.objects.all()
	context = {
		'testlist_dyntest' : testlist_dyntest,
		'testlist_dynmcqtest': testlist_dynmcqtest
	}
	return render(request, 'manage_tests/launch_test.html', context)	

def launch_specific_dyn_view(request, input_id_test):
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
	return render(request, 'manage_tests/launch_specific_dyn_test.html', context)	

def launch_specific_dynmcq_view(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	empty = True
	num_questions = get_questions(DynMCQTestInfo.questions)
	
	DynMCQquestions_List = []
	for i in range(len(num_questions)):
		DynMCQquestions_List.append(DynMCQquestion.objects.get(q_num = num_questions[i]))
		
	DynMCQanswers = []
	for i in range(len(num_questions)):
		theDynMCQanswers = DynMCQanswer.objects.filter(q_num = num_questions[i])
		for ans in theDynMCQanswers:
			DynMCQanswers.append(ans)
		
	#On ordonne les questions et les réponses dans une même liste pour l'affichage
	Questions_Answers_List = []
	for question in DynMCQquestions_List:
		Questions_Answers_List.append(question)
		DynMCQanswers = DynMCQanswer.objects.filter(q_num = question.q_num)
		for answer in DynMCQanswers:
			Questions_Answers_List.append(answer)
			
	group_names = []
	groups = Group.objects.all()
	for group in groups:
		if(group.name != "Teacher" and group.name != "Student"):
			group_names.append(group)
			
	form = DynMCQTestInfoForm_launch()
	choices = []
	for group in group_names:
		list = []
		list.append(group.name)
		list.append(group.name)
		choices.append(list)
	form.fields['activated_for'].choices = choices
	if request.method == 'POST':
		form = DynMCQTestInfoForm_launch(request.POST, instance = DynMCQTestInfo)
		choices = []
		for group in group_names:
			list = []
			list.append(group.name)
			list.append(group.name)
			choices.append(list)
		form.fields['activated_for'].choices = choices
	
		if form.is_valid():
			form.save()
			empty = False
			form = DynMCQTestInfoForm_launch()
			
	context = {
		'DynMCQquestions_List':DynMCQquestions_List,
		'DynMCQTestInfo':DynMCQTestInfo,
		'Questions_Answers_List': Questions_Answers_List,
		'form': form,
		'empty':empty,
	}
	return render(request, 'manage_tests/launch_specific_dynmcq_test.html', context)	

def in_launch_specific_dyn_view(request, input_id_test):
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
	return render(request, 'manage_tests/in_launch_specific_dyn_test.html', context)

def in_launch_specific_dynmcq_view(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	
	num_questions = get_questions(DynMCQTestInfo.questions)
	
	time = get_time(DynMCQTestInfo.time)
	
	DynMCQquestions_List = []
	for i in range(len(num_questions)):
		DynMCQquestions_List.append(DynMCQquestion.objects.get(q_num = num_questions[i]))
		
	DynMCQanswers = []
	for i in range(len(num_questions)):
		theDynMCQanswers = DynMCQanswer.objects.filter(q_num = num_questions[i])
		for ans in theDynMCQanswers:
			DynMCQanswers.append(ans)
		
	#On ordonne les questions et les réponses dans une même liste pour l'affichage
	Questions_Answers_List = []
	for question in DynMCQquestions_List:
		Questions_Answers_List.append(question)
		DynMCQanswers = DynMCQanswer.objects.filter(q_num = question.q_num)
		for answer in DynMCQanswers:
			Questions_Answers_List.append(answer)
		
	context = {
		'DynMCQquestions_List':DynMCQquestions_List,
		'DynMCQTestInfo':DynMCQTestInfo,
		'Questions_Answers_List': Questions_Answers_List,
		'time' : time,
	}
	return render(request, 'manage_tests/in_launch_specific_dynmcq_test.html', context)
	
def in_launch_mcq_stop_test(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	stop_mcq_test(DynMCQTestInfo)
	return redirect('/')
	
def get_time(time):
	timer = time.split(':')
	min = timer[0]
	sec = int(timer[1])/60
	sec = str(sec)
	sec = sec[1:]
	the_time = min + sec
	return the_time
	
def stop_mcq_test(DynMCQTestInfo):
	DynMCQTestInfo.activated_for = ""
	DynMCQTestInfo.time = ""
	DynMCQTestInfo.save()
	
	
def statistics_view(request, input_id_test):
	DynMCQTestInfo = get_object_or_404(DynMCQInfo, id_test=input_id_test)
	PassDynMCQInfo = Pass_DynMCQTest_Info.objects.filter(id_test = input_id_test)
	nb_questions = len(get_questions(DynMCQTestInfo.questions))
	
	PassDynMCQInfo_List = []
	for instance in PassDynMCQInfo:
		PassDynMCQInfo_List.append(instance)
	marks_list = []
	
	statistiques_notes = []
	i = 0
	while i <= int(nb_questions):
		statistiques_notes.append(0)
		i += 1
		
	for instance in PassDynMCQInfo_List:
		statistiques_notes[instance.mark] += 1
		marks_list.append(instance.mark)
	
	#Calcul de la moyenne et des notes hautes et basses
	note_plus_basse = Note_plus_basse(marks_list)
	note_plus_haute = Note_plus_haute(marks_list)

	moyenne_mcqtest = Moyenne(marks_list)
	nb_test = len(PassDynMCQInfo_List)
	
	#Calcul du 1er et du 3eme quartile du test
	q1 = Q1(marks_list)
	q3 = Q3(marks_list)

    #Calcul de la mediane
	m = Mediane(marks_list)
		
	#Calcul des fréquences
	total_freq = Frequences(statistiques_notes,PassDynMCQInfo_List)
	
	#On met dans une liste les statistiques liés à chaque question
	stats_question = Statistique_question(DynMCQTestInfo)
	
	#Pourcentage des statistiques par question
	pourcentage_question = Pourcentage_stats_question(stats_question,PassDynMCQInfo_List)
		
	total_statistics_question = []
	i = 0
	while i < len(stats_question):
		total_statistics_question.append((stats_question[i],pourcentage_question[i]))
		i += 1
	
	#Création des graphs
	GraphsQuestions(stats_question,int(nb_questions))
	GraphsNote(total_freq,int(nb_questions))
	GraphsBoxplot(marks_list)

	context = {
		'DynMCQTestInfo':DynMCQTestInfo,
		'PassDynMCQInfo_List': PassDynMCQInfo_List,
		'moyenne_mcqtest' : moyenne_mcqtest,
		'nb_test' : nb_test,
		'note_plus_haute' : note_plus_haute,
		'note_plus_basse' : note_plus_basse,
		'q1' : q1,
		'q3' : q3,
		'mediane' : m,
		'total_statistics_question' : total_statistics_question,
		'total_freq' : total_freq,
		'nb_questions':nb_questions,
	}
	return render(request, 'manage_tests/statistics.html', context)
	
def Moyenne(marks_list):
	moyenne = 0
	for mark in marks_list:
		moyenne += mark
	moyenne /= len(marks_list)
	moyenne="%.2f" % moyenne
	return moyenne
	
def Note_plus_basse(marks_list):
	note_plus_basse = 1000
	for mark in marks_list:
		if mark < note_plus_basse:
			note_plus_basse = mark
	return note_plus_basse
	
def Note_plus_haute(marks_list):
	note_plus_haute = 0
	for mark in marks_list:
		if mark > note_plus_haute:
			note_plus_haute = mark
	return note_plus_haute
	
def Q1(marks_list):
	marks_list.sort()
	if len(marks_list)%4 == 0:
		q1=marks_list[len(marks_list)//4-1]
	else:
		q1=marks_list[len(marks_list)//4]
	return q1
	
def Q3(marks_list):
	marks_list.sort()
	if len(marks_list)%4 == 0:
		q3=marks_list[3*len(marks_list)//4-1]
	else:
		q3=marks_list[3*len(marks_list)//4]
	return q3
	
def Mediane(marks_list):
	marks_list.sort()
	if len(marks_list)%2 == 0:
		m=((marks_list[(len(marks_list)-1)//2]+marks_list[len(marks_list)//2])/2)
	else:
		m = marks_list[len(marks_list)//2]
	return m
	
def Frequences(statistiques_notes,PassDynMCQInfo_List):
	total_freq = []
	somme_freq = 0
	for note in statistiques_notes:
		temp_freq = 100 * note / len(PassDynMCQInfo_List)
		somme_freq += temp_freq
		temp_freq = "%.2f" % temp_freq
		som_freq = "%.2f" % somme_freq
		total_freq.append((temp_freq,som_freq))
	return total_freq
	
def Statistique_question(DynMCQTestInfo):
	num_questions = get_questions(DynMCQTestInfo.questions)
	stats_question = []
	i = 0
	while i < int(len(num_questions)):
		stats_question.append(0)
		i += 1
		
	passdynmcqtest = Pass_DynMCQTest.objects.filter(id_test = DynMCQTestInfo.id_test)
	passdynmcqtest_List = []
	for instance in passdynmcqtest:
		passdynmcqtest_List.append(instance)
		
	for passdynmcq in passdynmcqtest_List:
		tmp_dynmcqtest = DynMCQanswer.objects.filter(q_num = passdynmcq.q_num, right_ans = 1)
		num_right_answers = []
		for ans in tmp_dynmcqtest:
			num_right_answers.append(ans.ans_num)
		#Si la réponse est bonne, on incrémente la note du test
		if check_answer(passdynmcq.r_ans,num_right_answers):
			index = 0
			for i in range(len(num_questions)):
				if(tmp_dynmcqtest[0].q_num == num_questions[i]):
					index = i
			stats_question[index] += 1
	return stats_question
	
def Pourcentage_stats_question(stats_question,PassDynMCQInfo_List):
	pourcentage_question = []
	for stat in stats_question:
		pourcentage = 100*stat/len(PassDynMCQInfo_List)
		pourcentage = "%.2f" % pourcentage
		pourcentage_question.append(pourcentage)
	return pourcentage_question
	
#Graphique statistiques par question
def GraphsQuestions(stats_question, nb_q):
	plt.rcdefaults()
	fig, ax = plt.subplots()

	questions = []
	i = 1
	while i <= nb_q:
		questions.append("q"+str(i))
		i += 1
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
def GraphsNote(total_freq,nb_q):
	labels = []
	i = 0
	while i <= nb_q:
		labels.append(str(i)+"/"+str(nb_q))
		i += 1
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
	



