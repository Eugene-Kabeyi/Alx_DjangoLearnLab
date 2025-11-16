# relationship_app/forms.py
from django import forms

class ExampleForm(forms.Form):
    q = forms.CharField(max_length=100, required=False)
