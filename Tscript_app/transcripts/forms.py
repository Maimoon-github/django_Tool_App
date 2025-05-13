from django import forms
from django.core.exceptions import ValidationError
from datetime import date

class AgeCalculatorForm(forms.Form):
    birth_date = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'max': date.today().isoformat(),
            'min': '1900-01-01',
        }),
        required=True,
        error_messages={'required': 'Please select your birth date.'}
    )

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date']
        if birth_date > date.today():
            raise ValidationError('Birth date cannot be in the future.')
        if birth_date < date(1900, 1, 1):
            raise ValidationError('Birth date cannot be before 1900.')
        return birth_date
