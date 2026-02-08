from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'ad_title', 'description', 'price', 'location', 'property_type', 'bhk', 
                  'bathrooms', 'furnishing', 'super_built_area', 'bachelors_allowed', 'total_floors', 
                  'facing', 'built_year', 'amenities']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Title'}),
            'ad_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Short ad title for listing'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the property...', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Rent'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address / City'}),
            'property_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Apartment, Villa'}),
            'bhk': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'furnishing': forms.Select(attrs={'class': 'form-control'}),
            'super_built_area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area in sqft', 'step': '0.01'}),
            'bachelors_allowed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'total_floors': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '100'}),
            'facing': forms.Select(attrs={'class': 'form-control'}),
            'built_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2020', 'min': '1900', 'max': '2030'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Wi-Fi, Parking, Gym (comma separated)', 'rows': 2}),
        }