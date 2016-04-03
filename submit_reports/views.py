from django.shortcuts import render, render_to_response, RequestContext
from .forms import SubmitReportForm, AddPartnerForm
from .models import SubmitReport, Student, Faculty, Staff, Course
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib import auth
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required,user_passes_test, permission_required
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.


@login_required(redirect_field_name=None)
@user_passes_test(lambda u: u.is_superuser or u.student is not None, redirect_field_name=None,
	login_url='/accounts/login/')
def submit_page(request):
	'''Page for submitting records, accessible to student users'''
	student = Student.objects.get(user=request.user)
	form = SubmitReportForm(request.POST or None, student)
	form.fields['courses'].queryset = Course.objects.filter(students__in=[student])
	if form.is_valid():
		save_form = form.save(commit=False)
		save_form.submitter=student
		save_form.save()
		save_form.save_m2m()
		return HttpResponseRedirect('student_logged_in_page')
	return render_to_response("submit_report.html",
		locals(),
		context_instance=RequestContext(request))


class FacultyView(UserPassesTestMixin, ListView):
	"""Page for faculty to view student records"""
	model = SubmitReport
	template_name = 'faculty_view.html'
	paginate_by = 25

	def get_queryset(self):
		faculty = self.request.user.faculty
		self.courses = faculty.course_set.all()
		return SubmitReport.objects.filter(courses__in=self.courses).distinct()

	def test_func(self):
		return self.request.user.faculty is not None

class FacultyDetailView(UserPassesTestMixin, ListView):
	faculty = request.user.faculty
	courses = faculty.course_set.all()
	model = SubmitReport
	queryset = SubmitReport.objects.filter(courses__in=self.courses).distinct()
	template_name = 'faculty_detail_view.html'

	def test_func(self):
		return self.request.user.faculty is not None

#Related to login
##############################################################

def login_view(request):
	"""Page for logging in"""
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)


def auth_view(request):
	"""Redirects users after login, or if login fails"""
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/accounts/loggedin/')
	else:
		return HttpResponseRedirect('/accounts/invalid/')


def logout_view(request):
	"""Page for users which have just logged out"""
	auth.logout(request)
	return render_to_response('logout.html')

#Home pages for different users (and also bd login info)
###################################################################

@login_required
@user_passes_test(lambda u: u.is_superuser or u.student is not None)
def student_logged_in_view(request):
	"""Homepage for logged in users"""
	return render_to_response('loggedin.html',
		{'username': request.user.username})


def invalid_login_view(request):
	"""Page for users who have not successfully logged in"""
	return render_to_response('invalid_login.html')


@login_required
@user_passes_test(lambda u: u.is_superuser or u.adminstaff is not None)
def admin_home_view(request):
	"""Homepage for logged in admin"""
	return render_to_response('admin_loggedin.html',
		{'username': request.user.username})

#Views for doing the actual stuff that users want to do
##########################################################################

@login_required
@user_passes_test(lambda u: u.is_superuser or u.adminstaff is not None)
def add_partners_view(request):
	'''Page for adding partners'''
	form = AddPartnerForm(request.POST or None)
	if form.is_valid():
		save_form = form.save(commit=False)
		save_form.save()
		if '_add_another' in request.POST:
			return HttpResponseRedirect('/admin/add_partner')
		return HttpResponseRedirect('admin_home_page')
	return render_to_response("add_partner.html",
		locals(),
		context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.is_superuser or u.adminstaff is not None)
def add_student_view(request):
	'''Page for adding partners'''
	form = AddPartnerForm(request.POST or None)
	if form.is_valid():
		save_form = form.save(commit=False)
		save_form.save()
		if '_add_another' in request.POST:
			return HttpResponseRedirect('/admin/add_student')
		return HttpResponseRedirect('admin_home_page')
	return render_to_response("add_student.html",
		locals(),
		context_instance=RequestContext(request))