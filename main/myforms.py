from django import forms

class FullTextSearchForm(forms.Form):
    s = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'size':'40'}))

