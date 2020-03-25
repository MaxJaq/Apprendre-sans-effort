from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

## Standard tests ##
			
class DynMCQInfo(models.Model):
	"""Main model for test : 
	DynMCQInfo gather the general informations on the test.

	Attributes :

	id_test (string) : id of the test, primary_key
	title (string) : title of the test
	questions (string) : list of id questions of the test (a[1,4,6]b[8,1,2] => a is for QCM questions and b for normal questions)
	time (string) : time for pass the test (5:30 => 5 min 30 sec)
	activated_for (string) : list of groups that can pass the test 
	release_time (string) : date of the release time of the test

	Function linked to the model :

	get_absolute_url : render the page to create the test
	get_absolute_url_q_menu : render the page to managing the test
	get_absolute_url_display : render the page to display the test
	question_reallocation : render the page to reallocate the questions
	get_statistics : render the page to show the statistics of the test
	launch_home: render the page to launch tests
	get_launch : render the page to launch the test
	get_in_launch : render the page when the test is launch
	stop_launch : render the page to stop the test
	"""			
	
	id_test = models.CharField(max_length=10, primary_key=True)
	title = models.TextField()
	print_test = models.BooleanField(default=False)
	questions = models.TextField(default="")
	time = models.CharField(max_length=10,default="")
	activated_for = models.TextField(default="")
	release_time = models.CharField(max_length=15, default="")

	def get_absolute_url(self):
		return reverse('tests:Create DynMCQTest', kwargs={'input_id_test': self.id_test})
	
	def get_absolute_url_q_menu(self):
		return reverse('tests:SelectMenu DynMCQquestion', kwargs={'input_id_test': self.id_test})
		
	def get_absolute_url_display(self):
		return reverse('tests:Display DynMCQtest', kwargs={'input_id_test': self.id_test})
		
	def question_reallocation(self):
		return reverse('tests:Question_reallocation', kwargs={'input_id_test': self.id_test})
		
	def get_statistics(self):
		return reverse('tests:Statistics', kwargs={'input_id_test': self.id_test})
		
	def launch_home(self):
		return reverse('tests:Launch')

	def get_launch(self):
		return reverse('tests:Launch Specific McqDyn', kwargs={'input_id_test': self.id_test})

	def get_in_launch(self):
		print_test = True
		return reverse('tests:In Launch Specific DynMcq', kwargs={'input_id_test': self.id_test})
		
	def stop_launch(self):
		return reverse('tests:Stop mcq launch', kwargs={'input_id_test': self.id_test})
		
		
class Dynquestion(models.Model):
	"""Model of the first type of question, the normal question with text answer :
	
	Attributes :
	
	q_num (int) : id of the question (primary_key)
	q_text (string) : question text
	r_text (string) : answer text of the question
	activated (int) : to activate the question or not (1 or 0)
	difficulty (string) : list of difficulties depending to themes ([2,0,4,0,1] => difficulty 2 for theme 1, difficulty 0 for theme 2 ...)
	
	Function linked to the model :

	get_absolute_url_question : render the page to create the question
	get_absolute_url_difficulty : render the page to add the difficulty to the question
	get_absolute_url_edit : render the page to edit the question
	get_absolute_url_delete : render the page to delete the question
	"""
	q_num = models.AutoField(primary_key=True)
	q_text = models.TextField()
	r_text = models.TextField()
	activated = models.IntegerField(null = True)
	difficulty = models.TextField(default="")

	def get_absolute_url_question(self):
		return reverse('tests:Create Dynquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_difficulty(self):
		return reverse('tests:Add Difficulty question', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit Dynquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete Dynquestion', kwargs={'input_q_num': self.q_num})	
		
class DynMCQquestion(models.Model):
	"""Model of the second type of question, the MCQ question with multiple choice answers :
	
	Attributes :
	
	q_num (int) : id of the question (primary_key)
	q_text (string) : question text
	nb_ans (string) : number of answers
	activated (int) : to activate the question or not (1 or 0)
	difficulty (string) : list of difficulties depending to themes ([2,0,4,0,1] => difficulty 2 for theme 1, difficulty 0 for theme 2 ...)
	
	Function linked to the model :

	get_absolute_url_question : render the page to create the question
	get_absolute_url_answers : render the page to create the answers of the question
	get_absolute_url_difficulty : render the page to add the difficulty to the question
	get_absolute_url_edit : render the page to edit the question
	get_absolute_url_delete : render the page to delete the question
	get_absolute_url_add_answer : render the page to add an answer to the question
	"""
	q_num = models.AutoField(primary_key=True)
	q_text = models.TextField()
	nb_ans = models.CharField(max_length=10)
	right_ans = models.IntegerField(null = True)
	activated = models.IntegerField(null = True)
	difficulty = models.TextField(default="")
		
	def get_absolute_url_question(self):
		return reverse('tests:Create DynMCQquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_answers(self):
		return reverse('tests:Create DynMCQanswers', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_difficulty(self):
		return reverse('tests:Add Difficulty', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit DynMCQquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete DynMCQquestion', kwargs={'input_q_num': self.q_num})
		
	def get_absolute_url_add_answer(self):
		return reverse('tests:AddAnswer DynMCQanswer', kwargs={'input_q_num': self.q_num})
		
		
class DynMCQanswer(models.Model):
	"""Model for the answers of DynMCQquestion :
	
	Attributes :
	
	q_num (int) : id of the question
	ans_num (int) : number of the answer
	ans_text (string) : text of the answer
	right_ans (int) : 1 if right answer, 0 if not
	
	Function linked to the model :

	get_absolute_url_edit : render the page to edit the answer
	get_absolute_url_delete : render the page to delete the answer
	"""
	q_num = models.IntegerField(null = True)
	ans_num = models.IntegerField(null = True)
	ans_text = models.TextField()
	right_ans = models.IntegerField()
		
	class Meta:
		unique_together = ('q_num', 'ans_num')
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit DynMCQanswer', kwargs={'input_q_num': self.q_num,'input_ans_num': self.ans_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete DynMCQanswer', kwargs={'input_q_num': self.q_num,'input_ans_num': self.ans_num})
		
class Pass_DynMCQTest_Info(models.Model):
	"""Main model for test answers of the user : 
	Pass_DynMCQTest_Info gather the general informations on the test.
	
	Attributes :
	
	id_test (string) : id of the passing test (DynMCQInfo id_test)
	id_student (string) : id of the student
	attempt (int) : number of attempt of the user on this test
	mark (int) : mark of the pass test
	time (string) : released time of the pass test
	
	Function linked to the model :

	get_absolute_url : render the page to pass the test
	get_absolute_url_display : render the page to display the pass test
	"""
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10, null=True)
	attempt = models.IntegerField(null = True)
	mark = models.IntegerField(null = True)
	time = models.CharField(max_length=15, null=True)
	
	class Meta:
		unique_together = ('id_test', 'id_student','attempt')
		
	def get_absolute_url(self):
		return reverse('tests:Pass dynmcqtest', kwargs={'input_id_test': self.id_test,'input_id_student': self.id_student,'input_attempt':self.attempt})
		
	def get_absolute_url_display(self):
		return reverse('tests:Display pass dynmcqtest', kwargs={'input_id_test': self.id_test,'input_id_student': self.id_student,'input_attempt':self.attempt})
		
class Pass_DynMCQTest(models.Model):
	"""Model of question answers of DynMCQquestion : 
	
	Attributes :
	
	id_test (string) : id of the passing test (DynMCQInfo id_test)
	id_student (string) : id of the student
	attempt (int) : number of attempt of the user on this test
	q_num (string) : id of the MCQ question
	r_ans (string) : list of number of the answers ([1,2] when checking first and second answer)
	"""
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10, null=True)
	attempt = models.IntegerField(null = True)
	q_num = models.CharField(max_length=10, null=True)
	r_ans = models.TextField()

	class Meta:
		unique_together = ('id_test', 'id_student','attempt','q_num')
		
class Pass_DynquestionTest(models.Model):
	"""Model of question answers of Dynquestion : 
	
	Attributes :
	
	id_test (string) : id of the passing test (DynMCQInfo id_test)
	id_student (string) : id of the student
	attempt (int) : number of attempt of the user on this test
	q_num (string) : id of the normal question
	r_answer (string) : text of the answer
	"""
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10, null=True)
	attempt = models.IntegerField(null = True)
	q_num = models.CharField(max_length=10, null=True)
	r_answer = models.TextField()

	class Meta:
		unique_together = ('id_test', 'id_student','attempt','q_num')


