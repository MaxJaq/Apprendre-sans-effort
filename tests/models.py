from django.db import models
from django.urls import reverse

# Create your models here.

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
