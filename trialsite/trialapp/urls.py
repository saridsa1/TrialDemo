from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth.decorators import login_required
app_name = 'trialapp'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
	path('login/',LoginView.as_view(), name='login'),
    path('loginsuccess/', views.login_success, name='login_success'),
	path('logout/',views.logout, name='logout'),
    # Investigator
	path('trials/edit/<int:id>',views.edit, name='edit'),
    path('operators/edit/<int:id>',views.Edit_Operator.as_view(), name='edit_operator'),
    path('update/<int:id>', views.update, name='update'),
    #path('updateoperator/<int:id>', views.update_operator, name='update_operator'),
    path('add_trials/', views.Add_Trials.as_view(), name='add_trials'),
    path('trials/', views.Trials.as_view(), name='trials'),
    path('trials/delete/<int:id>', views.delete, name='delete'),
    path('operators/delete/<int:id>', views.Delete_Operator.as_view(), name='delete_operator'),
    path('investigatordashboard/', views.investigator_dashboard, name='investigator_dashboard'),
    path('investigatorsignup/', views.InvestigatorSignup.as_view(), name='investigator_signup'),
    # Operator
    path('operatordashboard/', views.operator_dashboard, name='operator_dashboard'),
    path('operatorsignup/', views.OperatorSignup.as_view(), name='operator_signup'),
    path('operators/', views.Operators.as_view(), name='operators'),
    # Patient
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('patienttrials/', views.Patient_Trials.as_view(), name='patienttrials'),
    path('patients/', views.Patients.as_view(), name='patients'),
    #enrollment
    path('patienttrials/enroll/<int:id>',views.enroll, name='enroll'),
    path('patienttrials/enroll/', views.enrollment, name='enrollment'),
    path('import/', views.simple_upload, name='import'),
    path('download/', views.download_header, name='download_trialheader'),
    path('downloadtrials/', views.download_trials, name='download_trials'),
    path('forgot/', views.forgot_pass, name='forgot'),
    path('email/', views.send_email, name='email'),
    path('sendmail/', views.SendEmail.as_view(), name='send_mail'),

]
