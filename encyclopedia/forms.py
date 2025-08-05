from django import forms

class PageForm(forms.Form):
    title = forms.CharField(max_length=100, label="Título de la página", widget=forms.TextInput(attrs={
            'placeholder': "Ej: JavaScript, Python, Django...",
            'class': 'border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight mt-2 mb-6 focus:outline-none focus:border-blue-500'
        }))
    content = forms.CharField(label="Contenido de la página", widget=forms.Textarea(
        attrs={
            'rows': 12, 
            'placeholder': "## Hola mundo.",
            'class': 'border border-gray-300 rounded-lg w-full py-2 px-3 text-gray-700 leading-tight mt-2 mb-4 focus:outline-none focus:border-blue-500'
        }
    ))