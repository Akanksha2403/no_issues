from django import forms
from django.utils.timezone import now, timedelta
from .models import Complain

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
        if response_date <= forms.DateField().clean(now().date() + timedelta(days=1)):
            raise forms.ValidationError(
                "Response date must be at least one day after today.")
        return response_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['heading'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'rows': 5})
        self.fields['registered_to'].widget.attrs.update({'class': 'form-control'})
