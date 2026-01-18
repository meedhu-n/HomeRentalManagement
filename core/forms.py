from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'location', 'property_type', 'amenities']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the property...', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Rent'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address / City'}),
            'property_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Apartment, Villa'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Wi-Fi, Parking, Gym (comma separated)', 'rows': 2}),
        }