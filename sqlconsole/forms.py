from django import forms

class SQLConsoleForm(forms.Form):
    query = forms.CharField()
