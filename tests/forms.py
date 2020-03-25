from django import forms
from .models import (
	DynMCQInfo,
	DynMCQquestion,
	DynMCQanswer,
	Pass_DynMCQTest,
	Pass_DynMCQTest_Info,
	Dynquestion,
	Pass_DynquestionTest,
)

from .backend_code import compare_input_wt_expected as compare
		
class DynMCQTestInfoForm(forms.ModelForm):
	"""Form to fill id_test and title of the DynMCQInfo test
	"""
	id_test = forms.CharField(required=True)
	title = forms.CharField(required=True)
	class Meta:
		model = DynMCQInfo
		fields = [
			'id_test',
			'title',
		]

class DynMCQTestInfoForm_questions(forms.ModelForm):
	"""Form to fill the question numbers of the DynMCQInfo test (MultipleChoiceField with Checkbox)
	"""
	questions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = DynMCQInfo
		fields = [
			'questions',
		]
	
class DynMCQTestInfoForm_launch(forms.ModelForm):
	"""Form to fill activated_for and time attribute when lauching the DynMCQInfo test 
	"""
	activated_for = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
	time = forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'mm:ss'}))

	class Meta:
		model = DynMCQInfo
		fields = [
			'time',
			'activated_for',
		]
		
class MCQQuestion_difficulty_form(forms.ModelForm):
	"""Form to fill the difficulty of a DynMCQquestion question
	"""
	difficulty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
	class Meta:
		model = DynMCQquestion
		fields = [
			'difficulty',
		]
		
class Question_difficulty_form(forms.ModelForm):
	"""Form to fill the difficulty of a Dynquestion question
	"""
	difficulty = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())
	class Meta:
		model = Dynquestion
		fields = [
			'difficulty',
		]
		
class DynMCQquestionForm(forms.ModelForm):
	"""Form to fill the q_text, nb_ans, activated attribute of a DynMCQquestion question
	"""
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	nb_ans = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	class Meta:
		model = DynMCQquestion
		fields = [
			'q_text',
			'nb_ans',
			'activated',
		]
		
class DynquestionForm(forms.ModelForm):
	"""Form to fill the q_text, nb_ans, activated attribute of a Dynquestion question
	"""
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	r_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	class Meta:
		model = Dynquestion
		fields = [
			'q_text',
			'r_text',
			'activated',
		]
		
class DynMCQquestionForm_question(forms.ModelForm):
	"""Form to fill the q_text, activated attribute of a DynMCQquestion question when editing the question
	"""
	q_text = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':100}))
	activated = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'0 if no, 1 if yes'}))

	class Meta:
		model = DynMCQquestion
		fields = [
			'q_text',
			'activated',
		]

class DynMCQanswerForm(forms.ModelForm):
	"""Form to fill the ans_text, right_ans attribute of a DynMCQanswer answer
	"""
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
	"""Form to fill the r_ans of Pass_DynMCQTest when answering the test
	"""
	r_ans = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

	class Meta:
		model = Pass_DynMCQTest
		fields = [
			'r_ans',
		]
		
class Pass_DynquestionTestForm(forms.ModelForm):
	"""Form to fill the r_answer of Pass_DynquestionTest when answering the test
	"""
	r_answer = forms.CharField(widget=forms.Textarea(attrs={'rows':1, 'cols':25}))

	class Meta:
		model = Pass_DynquestionTest
		fields = [
			'r_answer',
		]
