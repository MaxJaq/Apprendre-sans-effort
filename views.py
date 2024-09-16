from django.shortcuts import render, get_object_or_404
from django.forms import formset_factory
from .forms import TestForm, PassTestForm, TestMcqForm, PassTestMcqForm, MCQTestForm, PassMCQTestForm, DynTestForm, DynTestFormShort,Pass_DynTestForm
from .models import Test_end_session, Pass_test_end_session, Test_mcq_end_session, MCQTest, Pass_MCQTest_end_session, DynTest,Pass_DynTest
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
	
def DynTest_create_view(request):
	form = DynTestForm(request.POST or None)
	if form.is_valid():
		form.save()
		form = DynTestForm()

	context = {
		'form': form
	}
	return render(request, 'manage_tests/test_create_dyntest.html',context)
	
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
	testlist_dyntest_all = DynTest.objects.all()
	form_questions = []
	nb_q = 0
	#On récupère les dynamics test et on compte le nombre de questions du test
	for dyntest in testlist_dyntest_all:
		if dyntest.id_test == input_id_test:
			form_questions.append(dyntest)
			nb_q += 1
	
	#On créé un formulaire groupé de pass_dyntest du nombre de question du test
	PassDynTestSet = formset_factory(Pass_DynTestForm, extra = nb_q)
	#on met dans data 3 propriétés obligatoire pour le fonctionnement du formulaire groupé
	data = {
		'form-TOTAL_FORMS': nb_q,
		'form-INITIAL_FORMS': '0',
		'form-MAX_NUM_FORMS': '',
	}
	form_answers = PassDynTestSet(data,request.POST)

	if form_answers.is_valid():
		for instance in form_answers:
			instance.save()
		form_answers = PassDynTestSet()

	context = {
		'form_answers': form_answers,
		'form_questions': form_questions,
	}
	return render(request, 'pass_tests/dyntest_pass.html', context)
	
def pass_testslist_teacher_view(request):
	# List all the pass tests of the db
	pass_tests_list_normal_questions = Pass_test_end_session.objects.all()
	pass_testlist_mcqtest = Pass_MCQTest_end_session.objects.all()
	context = {
		'pass_tests_list': pass_tests_list_normal_questions,
		'pass_tests_mcqtest_list': pass_testlist_mcqtest,
	}
	return render(request, 'manage_tests/pass_tests_list_teacher.html', context)



def tests_list_teacher_view(request):
	# List all the tests of the db
	tests_list_normal_questions = Test_end_session.objects.all()
	testlist_mcq = Test_mcq_end_session.objects.all()
	testlist_mcqtest = MCQTest.objects.all()
	testlist_dyntest_all = DynTest.objects.all()
	testlist_dyntest = []
	num_dyntest = []
	for dyntest in testlist_dyntest_all:
		if dyntest.id_test not in num_dyntest:
			num_dyntest.append(dyntest.id_test)
			testlist_dyntest.append(dyntest)
	context = {
		'tests_list': tests_list_normal_questions,
		'tests_mcq_list': testlist_mcq,
		'tests_mcqtest_list': testlist_mcqtest,
		'testlist_dyntest':testlist_dyntest,
	}
	return render(request, 'manage_tests/tests_list_teacher.html', context)

def tests_list_student_view(request):
	# List all the tests of the db
	tests_list_normal_questions = Test_end_session.objects.all()
	testlist_mcq = Test_mcq_end_session.objects.all()
	testlist_mcqtest = MCQTest.objects.all()
	testlist_dyntest_all = DynTest.objects.all()
	testlist_dyntest = []
	num_dyntest = []
	for dyntest in testlist_dyntest_all:
		if dyntest.id_test not in num_dyntest:
			num_dyntest.append(dyntest.id_test)
			testlist_dyntest.append(dyntest)
	context = {
		'tests_list': tests_list_normal_questions,
		'tests_mcq_list': testlist_mcq,
		'tests_mcqtest_list': testlist_mcqtest,
		'testlist_dyntest':testlist_dyntest,
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
	# Retrieve and display the requested mcq form
	testlist_dyntest_all = DynTest.objects.all()
	testlist_dyntest = []
	for dyntest in testlist_dyntest_all:
		if dyntest.id_test == input_id_test:
			testlist_dyntest.append(dyntest)
	context = {
		'testlist_dyntest': testlist_dyntest
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
	



