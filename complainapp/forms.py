from django import forms
from .models import *
from django import forms
from django.utils.timezone import now, timedelta

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True, label="First Name", widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=True, label="Last Name", widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    email = forms.EmailField(max_length=100, required=True, label="Email", widget=forms.TextInput(
        attrs={'placeholder': 'someone@iiitl.ac.in', 'class': 'form-control'}))
    pass1 = forms.CharField(max_length=100, required=True, label="Enter Password", widget=forms.PasswordInput(
        attrs={'placeholder': '', 'class': 'form-control'}))
    pass2 = forms.CharField(max_length=100, required=True, label="Enter Your Password again", widget=forms.PasswordInput(
        attrs={'placeholder': '', 'class': 'form-control'}))


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Email', 'label': 'Email', 'class': 'form-control'}))
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'label': 'Password', 'class': 'form-control'}))


class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = ('heading', 'description', 'registered_to', 'response_date')
    response_date = forms.DateField(
        label='Response Date',
        help_text='Select a date at least one day after today',
        widget=forms.SelectDateWidget(),
        initial=now().date() + timedelta(days=1)
    )


    def clean_response_date(self):
        response_date = self.cleaned_data['response_date']
        if response_date < forms.DateField().clean(now().date() + timedelta(days=1)):
            raise forms.ValidationError(
                "Response date must be at least one day after today.")
        return response_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['heading'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control autoresize-textarea', 'rows': 5})
        self.fields['registered_to'].widget.attrs.update({'class': 'form-control'})
