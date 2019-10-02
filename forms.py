from django import forms
from .models import (
	Test_end_session,
	Pass_test_end_session,
	Test_mcq_end_session,
	Pass_test_mcq_end_session
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
