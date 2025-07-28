from django import forms

class PageForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 1,
        'cols': 1
    }))