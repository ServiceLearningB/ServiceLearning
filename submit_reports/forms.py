from django import forms
from django.forms import MultipleChoiceField
from django.forms import Textarea, ModelForm, widgets
from .models import SubmitReport, Partner
from django.db import models
from django.contrib.auth.models import User

class SubmitReportForm(forms.ModelForm):
	class Meta:
		model = SubmitReport
		fields = ['start_time', 'end_time', 'courses', 'service_type', 'summary']
		#exclude = ['submitter', 'status']
		widgets = {
			'summary': Textarea(attrs={'cols': 50, 'rows': 3}),
		}

		def clean(self):
			cleaned_data = super(SubmitReportForm, self).clean()
			start_time = cleaned_data['start_time']
			end_time = cleaned_data['end_time']

			if (end_time <= start_time):
				raise forms.ValidationError("Start time must come before end time.")


class AddPartnerForm(forms.ModelForm):
	class Meta:
		model = Partner
		fields = ['name', 'is_active']

class AddStudentForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name']