from django.db import models
from django.urls import reverse
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

# Create your models here.
"""
class Student(Group):
    class Meta:
		name = 'Student'
        permissions = [('can_pass_tests', 'Can pass tests')]

class Teacher(Group):
    class Meta:
		name = 'Teacher'
        permissions = [('can_create_tests', 'Can create tests'),('can_see_tests', 'Can see tests'),('can_see_stats', 'Can see stats')]
"""
		
## Standard tests ##

class Test_end_session(models.Model):
	"""
	Model for the tests:
	TODO: how to make a dynamic number of questions
	"""
	id_test = models.CharField(max_length=10, null=False, primary_key=True)
	title = models.CharField(max_length=50)
	q1 = models.TextField()
	q2 = models.TextField()
	q3 = models.TextField()
	q4 = models.TextField()
	q5 = models.TextField()
	q6 = models.TextField()
	q7 = models.TextField()
	q8 = models.TextField()
	q9 = models.TextField()
	q10 = models.TextField()

	def get_absolute_url(self):
		# dynamic (if 'my_app' is renamed in the url, it will adapt)
		return reverse('tests:Display test', kwargs={'input_id_test': self.id_test})


class Pass_test_end_session(models.Model):
	"""
	Model for the students records of passing the test
	"""
	id_test = models.CharField(max_length=10, null=False)
	id_student = models.CharField(max_length=10, null=False)
	q1 = models.TextField()
	q2 = models.TextField()
	q3 = models.TextField()
	q4 = models.TextField()
	q5 = models.TextField()
	q6 = models.TextField()
	q7 = models.TextField()
	q8 = models.TextField()
	q9 = models.TextField()
	q10 = models.TextField()

	def get_absolute_url(self):
		return reverse('tests:Display pass test', kwargs={'input_id_test': self.id_test})

	class Meta:
		unique_together = ('id_test', 'id_student')

	def test_dumb_id_student_not_admin(self):
		if not self.id_student == 'admin':
			return True
		else:
			return False


class MCQTest(models.Model):
	id_test = models.CharField(max_length=10, null=False, primary_key=True)
	title = models.CharField(max_length=50,null=False)
	
	q1 = models.TextField()
	r11 = models.TextField()
	r12 = models.TextField()
	r13 = models.TextField()
	r14 = models.TextField()
	r1 = models.IntegerField(null=False)
	
	q2 = models.TextField()
	r21 = models.TextField()
	r22 = models.TextField()
	r23 = models.TextField()
	r24 = models.TextField()
	r2 = models.IntegerField(null=False)
	
	q3 = models.TextField()
	r31 = models.TextField()
	r32 = models.TextField()
	r33 = models.TextField()
	r34 = models.TextField()
	r3 = models.IntegerField(null=False)
	
	q4 = models.TextField()
	r41 = models.TextField()
	r42 = models.TextField()
	r43 = models.TextField()
	r44 = models.TextField()
	r4 = models.IntegerField(null=False)
	
	q5 = models.TextField()
	r51 = models.TextField()
	r52 = models.TextField()
	r53 = models.TextField()
	r54 = models.TextField()
	r5 = models.IntegerField(null=False)

	def get_absolute_url(self):
		# dynamic (if 'my_app' is renamed in the url, it will adapt)
		return reverse('tests:Display MCQTest test', kwargs={'input_id_test': self.id_test})
	
	def get_statistics(self):
		# dynamic (if 'my_app' is renamed in the url, it will adapt)
		return reverse('tests:Statistics', kwargs={'input_id_test': self.id_test})
		
class Pass_MCQTest_end_session(models.Model):
	"""
	Model for the students records of passing the test
	"""
	id_test = models.CharField(max_length=10, null=False)
	id_student = models.CharField(max_length=10, null=False)
	id_MCQTest = models.CharField(max_length=10, null=False)
	q1 = models.IntegerField()
	q2 = models.IntegerField()
	q3 = models.IntegerField()
	q4 = models.IntegerField()
	q5 = models.IntegerField()
	mark = models.IntegerField(null=True)

	def get_absolute_url(self):
		return reverse('tests:Display pass mcqtest', kwargs={'input_id_test': self.id_test})

	class Meta:
		unique_together = ('id_test', 'id_student')

	def test_dumb_id_student_not_admin(self):
		if not self.id_student == 'admin':
			return True
		else:
			return False
			
class DynMCQInfo(models.Model):
	id_test = models.CharField(max_length=10, primary_key=True)
	title = models.TextField()
	nb_q = models.CharField(max_length=10)

	def get_absolute_url(self):
		return reverse('tests:Create DynMCQTest', kwargs={'input_id_test': self.id_test})
	
	def get_absolute_url_q_menu(self):
		return reverse('tests:SelectMenu DynMCQquestion', kwargs={'input_id_test': self.id_test})
		
	def get_absolute_url_add_question(self):
		return reverse('tests:AddQuestion DynMCQquestion', kwargs={'input_id_test': self.id_test})
		
	def get_absolute_url_display(self):
		return reverse('tests:Display DynMCQtest', kwargs={'input_id_test': self.id_test})
		
	def get_statistics(self):
		return reverse('tests:Statistics', kwargs={'input_id_test': self.id_test})
		
		
class DynMCQquestion(models.Model):
	id_test = models.CharField(max_length=10, null=True)
	q_num = models.IntegerField(null = True)
	q_text = models.TextField()
	nb_ans = models.CharField(max_length=10)
	right_ans = models.IntegerField(null = True)
	activated = models.IntegerField(null = True)
		
	def get_absolute_url_question(self):
		return reverse('tests:Create DynMCQquestion', kwargs={'input_id_test': self.id_test,'input_q_num': self.q_num})
		
	def get_absolute_url_answers(self):
		return reverse('tests:Create DynMCQanswers', kwargs={'input_id_test': self.id_test,'input_q_num': self.q_num})
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit DynMCQquestion', kwargs={'input_id_test': self.id_test,'input_q_num': self.q_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete DynMCQquestion', kwargs={'input_id_test': self.id_test,'input_q_num': self.q_num})
		
	def get_absolute_url_add_answer(self):
		return reverse('tests:AddAnswer DynMCQanswer', kwargs={'input_id_test': self.id_test,'input_q_num': self.q_num})
		
	class Meta:
		unique_together = ('id_test', 'q_num')
		
class DynMCQanswer(models.Model):
	id_test = models.CharField(max_length=10, null=True)
	q_num = models.IntegerField(null = True)
	ans_num = models.IntegerField(null = True)
	ans_text = models.TextField()
	right_ans = models.IntegerField()
		
	class Meta:
		unique_together = ('id_test', 'q_num', 'ans_num')
		
	def get_absolute_url_edit(self):
		return reverse('tests:Edit DynMCQanswer', kwargs={'input_id_test': self.id_test,'input_q_num': self.q_num,'input_ans_num': self.ans_num})
		
	def get_absolute_url_delete(self):
		return reverse('tests:Delete DynMCQanswer', kwargs={'input_id_test': self.id_test,'input_q_num': self.q_num,'input_ans_num': self.ans_num})
		
class Pass_DynMCQTest_Info(models.Model):
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
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10, null=True)
	attempt = models.IntegerField(null = True)
	q_num = models.CharField(max_length=10, null=True)
	r_ans = models.TextField()

	class Meta:
		unique_together = ('id_test', 'id_student','attempt','q_num')

class DynTestInfo(models.Model):
	id_test = models.CharField(max_length=10, null=False, primary_key=True)
	title = models.CharField(max_length=10, null=False)
	nb_q = models.CharField(max_length=10, null=False)

	def get_absolute_url(self):
		return reverse('tests:Create DynTest', kwargs={'input_id_test': self.id_test})
		
	def get_absolute_url_dyntest(self):
		return reverse('tests:Display dyntest', kwargs={'input_id_test': self.id_test})

			
class DynTest(models.Model):
	id_test = models.CharField(max_length=10,null = True)
	q_num = models.IntegerField(null = True)
	q_text = models.TextField()
	r_text = models.TextField()
	activated = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('tests:Display dyntest', kwargs={'input_id_test': self.id_test})

	class Meta:
		unique_together = ('id_test', 'q_num')
		
class Pass_DynTest(models.Model):
	id_test = models.CharField(max_length=10, null=True)
	id_student = models.CharField(max_length=10)
	q_num = models.CharField(max_length=10, null=True)
	r_text = models.TextField()

	def get_absolute_url(self):
		return reverse('tests:Display pass dyntest', kwargs={'input_id_student': self.id_student})

	class Meta:
		unique_together = ('id_test', 'id_student','q_num')
		
## Multiple tests ##

class Test_mcq_end_session(models.Model):
	"""
	Model for the tests_mcq_end_session:
	TODO: how to make a dynamic number of questions
	"""
	id_test = models.CharField(max_length=10, null=False)
	title = models.CharField(max_length=50)
	id_q = models.IntegerField(null=False)
	question = models.CharField(max_length=50, null=False)
	answer_num = models.IntegerField(null=False)
	answer_num_exp = models.IntegerField(null=False)
	answer_text_correspnd = models.TextField()

	def get_absolute_url(self):
		return reverse('tests:Display mcq test', kwargs={'input_id_test': self.id_test})

	def __str__(self):
		# dic_table = {
		# 	'id_test': self.id_test,
		# 	'id_q': self.id_q,
		# 	'title': self.title,
		# 	'question': self.question,
		# 	'answer_num': self.answer_num,
		# 	'answer_num_exp': self.answer_num_exp,
		# 	'answer_text_correspnd': self.answer_text_correspnd
		# }

		str_table = """
		id_test: {0};\n
		id_q: {1};\n
		title: {2};\n
		question: {3};\n
		""".format(
			self.id_test,
			self.id_q,
			self.title,
			self.question,
			)

		return str_table

	class Meta:
		unique_together = ('id_test', 'id_q')



class Pass_test_mcq_end_session(models.Model):
	"""
	Model for the students records of passing the test
	"""
	id_test = models.CharField(max_length=10, null=False)
	id_student = models.CharField(max_length=10, null=False)
	id_q = models.IntegerField(null=False)
	input_answer_num = models.IntegerField(null=False)

	def get_absolute_url(self):
		return reverse('tests:Display mcq test', kwargs={'input_id_test': self.id_test})

	class Meta:
		unique_together = ('id_test', 'id_student', 'id_q')




# Normalized implementation

class Test(models.Model):
	id_test = models.CharField(max_length=12, primary_key=True)
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.id_test


class Question(models.Model):
	id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
	id_question = models.CharField(max_length=12, primary_key=True)
	question_text = models.CharField(max_length=200)

	def __str__(self):
		output = "{}, {}".format(self.id_test, self.id_question)
		return output


class Choice(models.Model):
	id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
	id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
	id_choice = models.CharField(max_length=12, primary_key=True)
	choice_text = models.CharField(max_length=200)
	is_correct = models.BooleanField(default=False)

	def __str__(self):
		output = "{}, {}, {}".format(self.id_test, self.id_question, self.id_choice)
		return output
