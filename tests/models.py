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
		return reverse('tests:Display test', kwargs={'input_id_test': self.id_test})

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
