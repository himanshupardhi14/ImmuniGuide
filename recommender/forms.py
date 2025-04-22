# recommender/forms.py
from django import forms

class VaccineForm(forms.Form):
    AGE_UNITS = [
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years'),
    ]
    
    age = forms.IntegerField(
        min_value=0,
        label='Age',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'})
    )
    
    unit = forms.ChoiceField(
        choices=AGE_UNITS,
        label='Unit',
        widget=forms.Select(attrs={'class': 'form-control'})
    )