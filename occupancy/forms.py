from django import forms 

class SearchForm(forms.Form):
    abstract = forms.CharField(max_length=100)
    ligand   = forms.CharField(max_length=5)
