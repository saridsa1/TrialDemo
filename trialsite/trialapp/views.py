from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.views import LoginView
from .forms import SignupForm, TrialForm , InvestigatorSignupForm ,OperatorSignupForm
from .forms import TrialForm
from .models import Trial, User ,Enrollment
from django.contrib import messages

def index(request):
	return render(request,'trialapp/index.html')

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


def dashboard(request):
    
    return render(request, 'trialapp/dashboard.html')


def investigator_dashboard(request):
    trials = Trial.objects.filter(organiser=request.user).count()
    operators = User.objects.filter(is_staff = True).count()
    patients = User.objects.filter(is_staff = False, is_superuser = False).count()
    enrollments = Enrollment.objects.filter(trial_organiser=request.user).count()
    user =request.user
    return render(request, 'trialapp/investigator_dashboard.html',{'trials':trials,'operators':operators,'patients':patients,'enrollments':enrollments,'user':user})


def operator_dashboard(request):
    trials = Trial.objects.filter(organiser=request.user).count()
    patients = User.objects.filter(is_staff = False, is_superuser = False).count()
    enrollments = Enrollment.objects.filter(trial_operator=request.user).count()  
    return render(request, 'trialapp/operator_dashboard.html',{'trials':trials,'operators':operators,'patients':patients,'enrollments':enrollments})



def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form submission successful')
            return redirect('trialapp:login')
        else:
            form = SignupForm()
            args = {'form': form}
            return render(request, 'trialapp/signup.html', args)  
    else:
        form = SignupForm()
        args = {'form': form}
        return render(request, 'trialapp/signup.html', args)



def investigatorsignup(request):
    if request.method =='POST':
        form = InvestigatorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trialapp:login')
        else:
            return HttpResponse("Not Submitted")
    else:
        form = InvestigatorSignupForm()
        args = {'form': form}
        return render(request, 'trialapp/signup.html', args)


def operatorsignup(request):
    if request.method =='POST':
        form = OperatorSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('trialapp:login')
        else:
            return HttpResponse("Not Submitted")
    else:
        form = OperatorSignupForm()
        args = {'form': form}
        return render(request, 'trialapp/signup.html', args)


def operators(request):
    rows =User.objects.filter(is_staff = True)
    return render(request,'trialapp/operators.html', {'rows': rows})

def edit_operator(request,id):
    user = User.objects.get(id=id)
    context={'user':user}
    return render(request, 'trialapp/edit_operator.html',context)



# def update_operator(request,id):
#     user = User.objects.get(id=id)
#     user.username=request.POST.get('username', None)
#     user.first_name=request.POST.get('first_name', None)
#     user.last_name=request.POST.get('last_name', None)
#     user.email=request.POST.get('email', None)
#     user.save()
#     return HttpResponseRedirect(reverse('trialapp:operators'))


def delete_operator(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('trialapp:operators'))


def patients(request):
    rows =User.objects.filter(is_staff = False,is_superuser = False)
    return render(request,'trialapp/pateints.html', {'rows': rows})


def addtrials(request):
    
    if request.method == 'POST':
        
        form = TrialForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            pincode = form.cleaned_data['pincode']
            discription = form.cleaned_data['discription']
            email = form.cleaned_data['email']
            organiser = request.user
            operator = request.POST.get('optr')
                  
            t =Trial(title=title,address=address,city=city,country=country,pincode=pincode,discription=discription,email=email,organiser=organiser,operator=operator)
            t.save()
            return HttpResponseRedirect(reverse('trialapp:trials'))
    # if a GET (or any other method) we'll create a blank form
    else:
        rows =User.objects.filter(is_staff=True)
        form = TrialForm()
        user = request.user
        print(user)

    return render(request, 'trialapp/addtrials.html', {'form': form,'user':user,'rows':rows})


def trials(request):
    rows =Trial.objects.filter(organiser=request.user)
    return render(request,'trialapp/trials.html', {'rows': rows})


def patient_trials(request):
    rows =Trial.objects.all()
    return render(request,'trialapp/patient_trials.html', {'rows': rows})


def edit(request,id):
    trial = Trial.objects.get(id=id)
    context={'trial':trial}
    return render(request, 'trialapp/edit.html',context)



def update(request,id):
    trial = Trial.objects.get(id=id)
    trial.title=request.POST['title']
    trial.address=request.POST['address']
    trial.city=request.POST['city']
    trial.pincode=request.POST['pincode']
    trial.discription=request.POST['discription']
    trial.email=request.POST['email']
    trial.save()
    return HttpResponseRedirect(reverse('trialapp:trials'))


def delete(request,id):
    trial = Trial.objects.get(id=id)
    trial.delete()
    return HttpResponseRedirect(reverse('trialapp:trials'))


def enroll(request,id):
    patient_username = request.user
    email = request.user.email
    trial = Trial.objects.get(id=id)
    trial_title =trial.title
    trial_operator = trial.operator
    trial_organiser = trial.organiser
    enrollment = Enrollment(patient_username=patient_username,email=email,trial_title=trial_title,trial_operator =trial_operator,trial_organiser=trial_organiser)
    enrollment.save()
    enrollments = Enrollment.objects.filter(trial_organiser=request.user)
    enroll = Enrollment.objects.filter(patient_username=request.user)
    return render(request, 'trialapp/patient_enrolls.html', {'enrollments': enrollments, 'enroll': enroll})


def enrollment(request):
    enrollments = Enrollment.objects.filter(trial_organiser=request.user)
    enroll = Enrollment.objects.filter(patient_username=request.user)
    return render(request, 'trialapp/patient_enrolls.html',{'enrollments':enrollments,'enroll':enroll})



