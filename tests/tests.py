from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Pass_test_end_session,DynMCQInfo,DynMCQquestion,DynMCQanswer,Pass_DynMCQTest_Info,Pass_DynMCQTest
from django.test.utils import setup_test_environment
from tests.views import (
	Moyenne,
	Note_plus_basse,
	Note_plus_haute,
	Q1,
	Q3,
	Mediane,
	Frequences,
	Statistique_question,
)

# Create your tests here.
def setUp_marks():
	marks_list = [2,4,1,6,8,7,6,6,0,4,5]
	return marks_list
	
def setUp_test():
	#Création du test
	theDynMCQtestInfo = DynMCQInfo(id_test = "1", title = "Premier Test", nb_q = "3")
		
	q1 = DynMCQquestion(id_test = "1", q_num = 1, q_text = "Q1", nb_ans = "2")
	r11 = DynMCQanswer(id_test = "1", q_num = 1, ans_num = 1, ans_text = "r11", right_ans = 1)
	r12 = DynMCQanswer(id_test = "1", q_num = 1, ans_num = 2, ans_text = "r12", right_ans = 0)
		
	q2 = DynMCQquestion(id_test = "1", q_num = 2, q_text = "Q2", nb_ans = "3")
	r21 = DynMCQanswer(id_test = "1", q_num = 2, ans_num = 1, ans_text = "r21", right_ans = 0)
	r22 = DynMCQanswer(id_test = "1", q_num = 2, ans_num = 2, ans_text = "r22", right_ans = 0)
	r23 = DynMCQanswer(id_test = "1", q_num = 2, ans_num = 3, ans_text = "r23", right_ans = 1)
		
	q3 = DynMCQquestion(id_test = "1", q_num = 3, q_text = "Q3", nb_ans = "2")
	r31 = DynMCQanswer(id_test = "1", q_num = 3, ans_num = 1, ans_text = "r31", right_ans = 0)
	r32 = DynMCQanswer(id_test = "1", q_num = 3, ans_num = 2, ans_text = "r32", right_ans = 1)
		
	#Création des réponses
	p_test1 = Pass_DynMCQTest_Info(id_test = "1", id_student = "1")
	p_test11 = Pass_DynMCQTest(id_test = "1", id_student = "1", q_num = "1", r_ans = "1")#Bonne réponse
	p_test12 = Pass_DynMCQTest(id_test = "1", id_student = "1", q_num = "2", r_ans = "2")#Mauvaise réponse
	p_test13 = Pass_DynMCQTest(id_test = "1", id_student = "1", q_num = "3", r_ans = "1")#Mauvaise réponse
	
	p_test2 = Pass_DynMCQTest_Info(id_test = "1", id_student = "2")
	p_test21 = Pass_DynMCQTest(id_test = "1", id_student = "2", q_num = "1", r_ans = "1")#Bonne réponse
	p_test22 = Pass_DynMCQTest(id_test = "1", id_student = "2", q_num = "2", r_ans = "3")#Bonne réponse
	p_test23 = Pass_DynMCQTest(id_test = "1", id_student = "2", q_num = "3", r_ans = "2")#Bonne réponse
	
	p_test3 = Pass_DynMCQTest_Info(id_test = "1", id_student = "3")
	p_test31 = Pass_DynMCQTest(id_test = "1", id_student = "3", q_num = "1", r_ans = "1")#Bonne réponse
	p_test32 = Pass_DynMCQTest(id_test = "1", id_student = "3", q_num = "2", r_ans = "3")#Bonne réponse
	p_test33 = Pass_DynMCQTest(id_test = "1", id_student = "3", q_num = "3", r_ans = "1")#Mauvaise réponse
		
	#Saving
		
	theDynMCQtestInfo.save()
	q1.save()
	r11.save()
	r12.save()
	q2.save()
	r21.save()
	r22.save()
	r23.save()
	q3.save()
	r31.save()
	r32.save()
	p_test1.save()
	p_test11.save()
	p_test12.save()
	p_test13.save()
	p_test2.save()
	p_test21.save()
	p_test22.save()
	p_test23.save()
	p_test3.save()
	p_test31.save()
	p_test32.save()
	p_test33.save()
	

class DumbModelTests(TestCase):
	"""
    def test_dumb_class(self):
        
        test that id_student can not be 'admin'
        
        Pass_test_id_student_admin = Pass_test_end_session(id_student='admin')
        self.assertIs(Pass_test_id_student_admin.test_dumb_id_student_not_admin(), False)
	"""

	def test_Moyenne(self):
		marks_list = setUp_marks()
		moyenne = Moyenne(marks_list)
		self.assertEqual(moyenne,"4.45")
		
	def test_Note_plus_basse(self):
		marks_list = setUp_marks()
		note_plus_basse = Note_plus_basse(marks_list)
		self.assertEqual(note_plus_basse,0)
		
	def test_Note_plus_haute(self):
		marks_list = setUp_marks()
		note_plus_haute = Note_plus_haute(marks_list)
		self.assertEqual(note_plus_haute,8)
		
	def test_Q1(self):
		marks_list = setUp_marks()
		q1 = Q1(marks_list)
		self.assertEqual(q1,2)
		
	def test_Q3(self):
		marks_list = setUp_marks()
		q3 = Q3(marks_list)
		self.assertEqual(q3,6)
		
	def test_Mediane(self):
		marks_list = setUp_marks()
		median = Mediane(marks_list)
		self.assertEqual(median,5)
		
	def test_Frequences(self):
		statistique_notes = [1,1,1,0,2,1,3,1,1]
		total_freq = Frequences(statistique_notes,setUp_marks())
		
		freq = ["9.09","9.09","9.09","0.00","18.18","9.09","27.27","9.09","9.09"]
		cum_freq = ["9.09","18.18","27.27","27.27","45.45","54.55","81.82","90.91","100.00"]
		test_freq = []
		i = 0
		while i < len(freq):
			test_freq.append((freq[i],cum_freq[i]))
			i += 1
		self.assertEqual(total_freq,test_freq)
		
	def test_Statistique_question(self):
		setUp_test()
		theDynMCQtestInfo = get_object_or_404(DynMCQInfo, id_test = "1")
		
		stats_question = Statistique_question(theDynMCQtestInfo)
		test_stats_question = [3,2,1]
		
		self.assertEqual(stats_question,test_stats_question)
	
	#Test de la page de chargement des tests
	def test_Chargement_test(self):
		setUp_test()
		DynMCQtestInfo = get_object_or_404(DynMCQInfo, id_test = "1")
		response = self.client.get(reverse('tests:List tests teacher'))
		test = response.context['testlist_dynmcqtestinfo_all']
		self.assertEqual(test[0],DynMCQtestInfo)
		
	#Test de la page de chargement des pass tests
	def test_Chargement_pass_test(self):
		setUp_test()
		Pass_DynMCQtestInfo_all = Pass_DynMCQTest_Info.objects.all()
		response = self.client.get(reverse('tests:List pass tests teacher'))
		test = response.context['pass_dynMCQtest_all']
		test_list = []
		Pass_DynMCQtestInfo_all_list = []
		i = 0
		while i < len(test):
			test_list.append(test[i])
			Pass_DynMCQtestInfo_all_list.append(Pass_DynMCQtestInfo_all[i])
			i += 1
		self.assertEqual(test_list,Pass_DynMCQtestInfo_all_list)
		
	
		
