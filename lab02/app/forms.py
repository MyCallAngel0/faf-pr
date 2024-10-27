from django import forms
from .models import Laptop


class LaptopForm(forms.ModelForm):
    class Meta:
        model = Laptop
        fields = ['name', 'price', 'brand', 'currency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'currency': forms.Select(attrs={'class': 'form-control'}),
        }
