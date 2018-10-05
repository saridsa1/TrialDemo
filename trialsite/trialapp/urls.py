from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'trialapp'
urlpatterns = [
    path('', views.index, name='index'),
	path('login/',LoginView.as_view(), name='login'),
    path('loginsuccess/', views.login_success, name='login_success'),
	path('logout/',views.logout, name='logout'),
    # Investigator
	path('trials/edit/<int:id>',views.edit, name='edit'),
    path('operators/edit/<int:id>',views.edit_operator, name='edit_operator'),
    path('update/<int:id>', views.update, name='update'),
    #path('updateoperator/<int:id>', views.update_operator, name='update_operator'),
    path('add_trials/', views.addtrials, name='add_trials'),
    path('trials/', views.trials, name='trials'),
    path('trials/delete/<int:id>', views.delete, name='delete'),
    path('operators/delete/<int:id>', views.delete_operator, name='delete_operator'),
    path('investigatordashboard/', views.investigator_dashboard, name='investigator_dashboard'),
    path('investigatorsignup/', views.investigatorsignup, name='investigator_signup'),
    # Operator
    path('operatordashboard/', views.operator_dashboard, name='operator_dashboard'),
    path('operatorsignup/', views.operatorsignup, name='operator_signup'),
    path('operators/', views.operators, name='operators'),
    # Patient
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('patienttrials/', views.patient_trials, name='patienttrials'),
    path('patients/', views.patients, name='patients'),
    #enrollment
    path('patienttrials/enroll/<int:id>',views.enroll, name='enroll'),
    path('patienttrials/enroll/', views.enrollment, name='enrollment'),

]
