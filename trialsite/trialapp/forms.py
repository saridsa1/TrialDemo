from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

from tinymce.widgets import TinyMCE
from django_select2.forms import Select2MultipleWidget, Select2Widget


class TrialForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
        }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
        }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
        }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
        }))
    pincode = forms.CharField(widget=forms.NumberInput(attrs={
        'class':'form-control'
        }))
    discription = forms.CharField(widget=TinyMCE(attrs={'cols':10,'rows':30,'class':'my_tinymce'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class':'form-control'
        }))
    operator = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),widget=Select2Widget(attrs={'class':'form-control'}))
    # operators = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),widget=Select2MultipleWidget(attrs={'class':'form-control'}))




class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    # def clean_password2(self):
    #     # Check that the two password entries match
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passwords don't match")
    #     return password2
    # def save(self, commit=True):
    #     user = super(SignupForm, self).save(commit=False)
    #     user.username = self.cleaned_data['username']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.email = self.cleaned_data['email']
    #     user.password1 = self.cleaned_data['password1']
    #     user.save()
    #
    #     if commit:
    #         return user

class InvestigatorSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'is_superuser'
        )

    def save(self, commit=True):
        invest = super(InvestigatorSignupForm, self).save(commit=False)
        invest.username = self.cleaned_data['username']
        invest.first_name = self.cleaned_data['first_name']
        invest.last_name = self.cleaned_data['last_name']
        invest.email = self.cleaned_data['email']
        invest.password1 = self.cleaned_data['password1']
        invest.is_superuser = True
        invest.save()
        if commit:
            return invest

class OperatorSignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'is_staff',
            
        )

    def save(self,commit=True):
        optr = super(OperatorSignupForm, self).save(commit=False)
        optr.username = self.cleaned_data['username']
        optr.first_name = self.cleaned_data['first_name']
        optr.last_name = self.cleaned_data['last_name']
        optr.email = self.cleaned_data['email']
        optr.password1 = self.cleaned_data['password1']
        optr.is_staff = True
        optr.save()
        if commit:
            return optr

class ForgotpasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2',

        )

class MailForm(forms.Form):

    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    message = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email_list = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True),
                                      widget=Select2Widget(attrs={'class': 'form-control'}))