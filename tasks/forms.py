from django import forms

class TodoForm(forms.Form):
    add = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control m-auto',
        'placeholder': 'Add a new todo...'
    }))