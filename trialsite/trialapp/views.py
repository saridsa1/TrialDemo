from django.shortcuts import render, redirect, render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from .forms import SignupForm, TrialForm, InvestigatorSignupForm, OperatorSignupForm, ForgotpasswordForm, MailForm
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views.generic import View
from .models import Trial, Enrollment
from django.contrib import messages
import csv, io
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers

import json
class Index(TemplateView):
    template_name = 'trialapp/index.html'


def login_success(request):
    """
    Redirects users based on whether they are in the admins group
    """
    if request.user.is_superuser:
        # user is an admin
        return redirect("trialapp:investigator_dashboard")
    elif request.user.is_staff:
        # user is an operator
        return redirect("trialapp:operator_dashboard")
    else:
        # user is an pateint
        return redirect("trialapp:dashboard")


def logout(request):
    logout(request)
    return HttpResponseRedirect('trialapp:index')

class Dashboard(TemplateView):
    template_name = 'trialapp/dashboard.html'


def investigator_dashboard(request):
    trials = Trial.objects.filter(organiser=request.user).count()
    operators = User.objects.filter(is_staff=True).count()
    patients = User.objects.filter(is_staff=False, is_superuser=False).count()
    enrollments = Enrollment.objects.filter(trial_organiser=request.user).count()
    user = request.user
    return render(request, 'trialapp/investigator_dashboard.html',
                  {'trials': trials, 'operators': operators, 'patients': patients, 'enrollments': enrollments,
                   'user': user})


def operator_dashboard(request):
    trials = Trial.objects.filter(organiser=request.user).count()
    patients = User.objects.filter(is_staff=False, is_superuser=False).count()
    enrollments = Enrollment.objects.filter(trial_operator=request.user).count()
    return render(request, 'trialapp/operator_dashboard.html',
                  {'trials': trials, 'operators': operators, 'patients': patients, 'enrollments': enrollments})



class Signup(CreateView):
    template_name = 'trialapp/signup.html'
    success_url = '/trialapp/login/'
    form_class = SignupForm

class AjaxSignup(CreateView):
    template_name = 'trialapp/ajaxsignup.html'
    success_url = '/trialapp/login/'
    form_class = SignupForm

class InvestigatorSignup(CreateView):
    template_name = 'trialapp/signup.html'
    success_url = '/trialapp/login/'
    form_class = InvestigatorSignupForm


class OperatorSignup(CreateView):
    template_name = 'trialapp/signup.html'
    success_url = '/trialapp/investigatordashboard/'
    form_class = OperatorSignupForm


class Patients(ListView):
    model = User
    template_name = 'trialapp/operators.html'

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=False, is_superuser=False)
        return queryset


# class AjaxTrials(View):
#     model = Trial
#     template_name = 'trialapp/autocomp.html'
#
#     def get_queryset(self,query):
#         # data = Trial.objects.filter(string__icontains = query)
#         data = Trial.objects.all()
#         return data


def AjaxTrials(request):
    stxt =request.POST.get('txt')
    print(stxt)
    # data = serializers.serialize("json", Trial.objects.filter(title__icontains= stxt))
    if stxt != '':
        data=  Trial.objects.filter(title__istartswith = stxt);

        lst =[];
        for i in data:
            s={}
            s['title'] = i.title
            lst.append(s)
        return HttpResponse(lst)




class Add_Trials(FormView):
    template_name = 'trialapp/addtrials.html'
    # success_url = reverse_lazy('trialapp:trials')
    form_class = TrialForm

    def form_valid(self,form):
        title = form.cleaned_data['title']
        address = form.cleaned_data['address']
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']
        pincode = form.cleaned_data['pincode']
        discription = form.cleaned_data['discription']
        email = form.cleaned_data['email']
        organiser = self.request.user
        operator = form.cleaned_data['operator']
        print(operator, "hello")
        t = Trial(title=title, address=address, city=city, country=country, pincode=pincode,
                  discription=discription, email=email, organiser=organiser, operator=operator)
        t.save()
        return redirect('trialapp:investigator_dashboard')



class AjaxTemTrials(TemplateView):
    template_name = 'trialapp/autocomp.html'


class Trials(ListView):
    model = User
    template_name = 'trialapp/trials.html'

    def get_queryset(self):
        queryset = Trial.objects.all()
        return queryset

class Patient_Trials(ListView):
    model = Trial
    template_name = 'trialapp/patient_trials.html'

    def get_queryset(self):
        queryset = Trial.objects.all()
        return queryset




def edit(request, id):
    trial = Trial.objects.get(id=id)
    context = {'trial': trial}
    return render(request, 'trialapp/edit.html', context)


def update(request, id):
    trial = Trial.objects.get(id=id)
    trial.title = request.POST['title']
    trial.address = request.POST['address']
    trial.city = request.POST['city']
    trial.pincode = request.POST['pincode']
    trial.discription = request.POST['discription']
    trial.email = request.POST['email']
    trial.save()
    return HttpResponseRedirect(reverse('trialapp:trials'))


def delete(request, id):
    trial = Trial.objects.get(id=id)
    trial.delete()
    return HttpResponseRedirect(reverse('trialapp:trials'))


def enroll(request, id):
    patient_username = request.user
    email = request.user.email
    trial = Trial.objects.get(id=id)
    trial_title = trial.title
    trial_operator = trial.operator
    trial_organiser = trial.organiser
    enrollment = Enrollment(patient_username=patient_username, email=email, trial_title=trial_title,
                            trial_operator=trial_operator, trial_organiser=trial_organiser)
    enrollment.save()
    enrollments = Enrollment.objects.filter(trial_organiser=request.user)
    enroll = Enrollment.objects.filter(patient_username=request.user)
    return render(request, 'trialapp/patient_enrolls.html', {'enrollments': enrollments, 'enroll': enroll})


def enrollment(request):
    enrollments = Enrollment.objects.filter(trial_organiser=request.user)
    enroll = Enrollment.objects.filter(patient_username=request.user)
    return render(request, 'trialapp/patient_enrolls.html', {'enrollments': enrollments, 'enroll': enroll})


def simple_upload(request):
    template = "trialapp/import.html"
    if request.method == "GET":
        return render(request, template)

    csv_file = request.FILES['myfile']
    data_set = csv_file.read().decode('utf-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        created = Trial(title=column[0], address=column[1], city=column[2], country=column[3], pincode=column[4],
                        discription=column[5], email=column[6], operator=column[7], organiser=column[8])
        created.save()

    return render(request, template)


def download_header(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="trialheader.csv"'

    writer = csv.writer(response)
    cols = Trial._meta.get_fields()
    cn = []
    for f in cols:
        cn.append(f.name)
    cn.pop(0)
    writer.writerow(cn)

    return response


def download_trials(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alltrials.csv"'

    writer = csv.writer(response)
    cols = Trial._meta.get_fields()
    cn = []
    for f in cols:
        cn.append(f.name)
    writer.writerow(cn)
    trials = Trial.objects.all()
    for f in trials:
        writer.writerow(
            [f.id, f.title, f.address, f.city, f.country, f.pincode, f.discription, f.email, f.organiser, f.operator])

    return response


def forgot_pass(request):
    form = ForgotpasswordForm(request.POST)
    if request.method == 'POST':

        email = request.POST['email']
        user = User.objects.get(email=email)
        if user is not None:
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 and password2 and password1 == password2:
                user.set_password(password2)
                user.save()
            else:
                return render(request, 'trialapp/forgot.html', {'form': form})
            return redirect(reverse('trialapp:login'))

    else:
        return render(request, 'trialapp/forgot.html', {'form': form})



def send_email(request):
    subject = "thankyou for registraton"
    message = "thanks login plz"
    from_email = settings.EMAIL_HOST_USER
    to_list = ['ayazurrashid@gmail.com']
    send_mail(subject, message, from_email, to_list, fail_silently=False)
    print("send")
    return HttpResponse("Mail Sent")


class SendEmail(FormView):
    template_name = 'trialapp/email.html'
    form_class = MailForm
    success_url = 'index/'

    def form_valid(request,form):
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        username = form.cleaned_data['email_list']
        to_list=[]
        user = User.objects.get(username=username)
        to_list.append(user.email)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        return redirect('trialapp:investigator_dashboard')




class Delete_Operator(DeleteView):
    model = User
    success_url = reverse_lazy('operators')

    def get_queryset(id):
        queryset = User.objects.get(id=id)
        queryset.delete()
        return queryset


def delete_operator(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('trialapp:operators'))


class Operators(ListView):
    model =  User
    template_name = 'trialapp/operators.html'

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=True)
        return queryset

def edit_operator(request, id):
    user = User.objects.get(id=id)
    context = {'user': user}
    return render(request, 'trialapp/edit_operator.html', context)

class Edit_Operator(UpdateView):
    template_name = 'trialapp/edit_operator.html'
    model = User
    success_url = reverse_lazy('operators')

# def patient_trials(request):
#     rows = Trial.objects.all()
#     return render(request, 'trialapp/patient_trials.html', {'rows': rows})


# def addtrials(request):
#     if request.method == 'POST':
#
#         form = TrialForm(request.POST)
#
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             address = form.cleaned_data['address']
#             city = form.cleaned_data['city']
#             country = form.cleaned_data['country']
#             pincode = form.cleaned_data['pincode']
#             discription = form.cleaned_data['discription']
#             email = form.cleaned_data['email']
#             organiser = request.user
#             operator = form.cleaned_data['operator']
#             print(operator, "hello")
#             t = Trial(title=title, address=address, city=city, country=country, pincode=pincode,
#                       discription=discription, email=email, organiser=organiser, operator=operator)
#             t.save()
#             return HttpResponseRedirect(reverse('trialapp:trials'))
#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = TrialForm()
#         # user = request.user
#     return render(request, 'trialapp/addtrials.html', {'form': form})


# def signup(request):
#     if request.method == 'POST':
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Form submission successful')
#             return redirect('trialapp:login')
#         else:
#             form = SignupForm()
#             args = {'form': form}
#             return render(request, 'trialapp/signup.html', args)
#     else:
#         form = SignupForm()
#         args = {'form': form}
#         return render(request, 'trialapp/signup.html', args)


# def investigatorsignup(request):
#     if request.method == 'POST':
#         form = InvestigatorSignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('trialapp:login')
#         else:
#             return HttpResponse("Not Submitted")
#     else:
#         form = InvestigatorSignupForm()
#         args = {'form': form}
#         return render(request, 'trialapp/signup.html', args)


# def operatorsignup(request):
#     if request.method == 'POST':
#         form = OperatorSignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('trialapp:login')
#         else:
#             return HttpResponse("Not Submitted")
#     else:
#         form = OperatorSignupForm()
#         args = {'form': form}
#         return render(request, 'trialapp/signup.html', args)



# def operators(request):
#     rows = User.objects.filter(is_staff=True)
#     return render(request, 'trialapp/operators.html', {'rows': rows})


# def update_operator(request,id):
#     user = User.objects.get(id=id)
#     user.username=request.POST.get('username', None)
#     user.first_name=request.POST.get('first_name', None)
#     user.last_name=request.POST.get('last_name', None)
#     user.email=request.POST.get('email', None)
#     user.save()
#     return HttpResponseRedirect(reverse('trialapp:operators'))



# def patients(request):
#     rows = User.objects.filter(is_staff=False, is_superuser=False)
#     return render(request, 'trialapp/pateints.html', {'rows': rows})

