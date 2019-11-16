from django import forms
from .models import (
	Test_end_session,
	Pass_test_end_session,
	Test_mcq_end_session,
	Pass_test_mcq_end_session,
	MCQTest,
	Pass_MCQTest_end_session,
	DynTest,
	Pass_DynTest,
	DynTestInfo,
	DynMCQInfo,
	DynMCQquestion,
	DynMCQanswer,
	Pass_DynMCQTest,
)

from .backend_code import compare_input_wt_expected as compare


class TestForm(forms.ModelForm):
	# Properly displayed
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Test title'}))
	q1 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q2 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q3 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q4 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q5 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q6 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q7 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q8 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q9 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q10 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))

	# Robustly Handled
	class Meta:
		model = Test_end_session
		fields = [
			'id_test',
			'title',
			'q1',
			'q2',
			'q3',
			'q4',
			'q5',
			'q6',
			'q7',
			'q8',
			'q9',
			'q10'
		]
	

class PassTestForm(forms.ModelForm):
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	id_student = forms.CharField(required=True)
	q1 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q2 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q3 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q4 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q5 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q6 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q7 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q8 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q9 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	q10 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))

	# Robustly Handled
	class Meta:
		model = Pass_test_end_session
		fields = [
			'id_test',
			'id_student',
			'q1',
			'q2',
			'q3',
			'q4',
			'q5',
			'q6',
			'q7',
			'q8',
			'q9',
			'q10'
		]


	# Validate data  
	def clean_data(self, *args, **kwargs):
		# TODO: make coherent tests (that are valid for any domain of learning)
	
		id_test = self.cleaned_data.get('id_test')
		id_student = self.cleaned_data.get('id_student')

		if not 'id' in id_test:
			raise forms.ValidationError('This is not a valide test id')

		if not 'stu' in id_student:
			raise forms.ValidationError('This is not a valid student id')
		
		return True


	def assess_answer(self, *args, **kwargs):
		# Retrieve expected answer and format from the db.
		# Compare wt. the answer and yield a grade accordingly
		# TODO: handle it for each questions, since it is currently
		# handling the whole form, although the comparison is supposed
		# to be made on a unique question.
		
		self.clean_data()

		INPUT_EXPECTED = 'TODO: retrieve exp answer in db'
		SPLIT_ARGS = 'TODO: retrieve args in db'
		INPUT_ENTERED = 'TODO: use input data in the form'

		grade = compare(
			input_expected=INPUT_EXPECTED,
			input_entered=SPLIT_ARGS,
			split_args=INPUT_ENTERED
		)

		# TODO: make a static sheet in the db with constants
		PASS_SCORE = 0.8
		
		if grade >= PASS_SCORE:
			assessment = {
				'grade':grade,
				'comment':'pass'
			}
		else:
			assessment = {
				'grade':grade,
				'comment':'retry'
			}
			
		return assessment

class MCQTestForm(forms.ModelForm):
	# Properly displayed
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Test title'}))
	q1 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r11 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r12 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r13 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r14 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	
	q2 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r21 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r22 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r23 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r24 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	
	q3 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r31 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r32 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r33 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r34 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r3 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	
	q4 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r41 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r42 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r43 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r44 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r4 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	
	q5 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r51 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r52 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r53 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r54 = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':20}))
	r5 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	

	# Robustly Handled
	class Meta:
		model = MCQTest
		fields = [
			'id_test',
			'title',
			'q1',
			'r11',
			'r12',
			'r13',
			'r14',
			'r1',
			'q2',
			'r21',
			'r22',
			'r23',
			'r24',
			'r2',
			'q3',
			'r31',
			'r32',
			'r33',
			'r34',
			'r3',
			'q4',
			'r41',
			'r42',
			'r43',
			'r44',
			'r4',
			'q5',
			'r51',
			'r52',
			'r53',
			'r54',
			'r5',
		]
		
class PassMCQTestForm(forms.ModelForm):
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	id_student = forms.CharField(required=True)
	id_MCQTest = forms.CharField(required=True)
	q1 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	q2 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	q3 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	q4 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))
	q5 = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Numéro de la bonne réponse'}))

	# Robustly Handled
	class Meta:
		model = Pass_MCQTest_end_session
		fields = [
			'id_test',
			'id_student',
			'id_MCQTest',
			'q1',
			'q2',
			'q3',
			'q4',
			'q5',
		]
		


## Multiple choices forms ##

# TODO: create dynamic number of questions
class TestMcqForm(forms.ModelForm):
	# Properly displayed
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Test title'}))
	id_q = forms.IntegerField()
	question = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Question to the student'}))
	answer_num = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Possible choice number")
	answer_num_exp = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Choice expected number")
	answer_text_correspnd = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Corresponding answer'}))

	# Robustly Handled
	class Meta:
		model = Test_mcq_end_session
		fields = [
			'id_test',
			'title',
			'id_q',
			'question',
			'answer_num',
			'answer_num_exp',
			'answer_text_correspnd'
		]
		
class DynTestForm(forms.ModelForm):
	# Properly displayed
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))
	activated = forms.BooleanField(initial=False)

	# Robustly Handled
	class Meta:
		model = DynTest
		fields = [
			'q_text',
			'r_text',
			'activated',
		]
		
		
class DynTestInfoForm(forms.ModelForm):
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	title = forms.CharField(required=True)
	nb_q = forms.CharField(required=True)
	class Meta:
		model = DynTestInfo
		fields = [
			'id_test',
			'title',
			'nb_q',
		]
		
class Pass_DynTestForm(forms.ModelForm):
	id_student = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Student ID'}))
	r_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))

	class Meta:
		model = Pass_DynTest
		fields = [
			'id_student',
			'r_text',
		]
		
class DynMCQTestInfoForm(forms.ModelForm):
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	title = forms.CharField(required=True)
	nb_q = forms.CharField(required=True)
	class Meta:
		model = DynMCQInfo
		fields = [
			'id_test',
			'title',
			'nb_q',
		]
		
class DynMCQquestionForm(forms.ModelForm):
	# Properly displayed
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	nb_ans = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	# Robustly Handled
	class Meta:
		model = DynMCQquestion
		fields = [
			'q_text',
			'nb_ans',
			'activated',
		]
		
class DynMCQquestionForm_question(forms.ModelForm):
	# Properly displayed
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	# Robustly Handled
	class Meta:
		model = DynMCQquestion
		fields = [
			'q_text',
			'activated',
		]

class DynMCQanswerForm(forms.ModelForm):
	# Properly displayed
	ans_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	right_ans = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))
	
	# Robustly Handled
	class Meta:
		model = DynMCQanswer
		fields = [
			'ans_text',
			'right_ans',
		]

class Pass_DynMCQTestForm(forms.ModelForm):
	id_student = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Student ID'}))
	r_num = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':10}))

	class Meta:
		model = Pass_DynMCQTest
		fields = [
			'id_student',
			'r_num',
		]

class PassTestMcqForm(forms.ModelForm):
	id_test = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'test id'}))
	id_student = forms.CharField(required=True)
	q_num = forms.IntegerField()
	select_answer_num = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, label="Q1")

	# Robustly Handled
	class Meta:
		model = Pass_test_mcq_end_session
		fields = [
			'id_test',
			'id_student',
			'q_num',
			'select_answer_num'
		]
