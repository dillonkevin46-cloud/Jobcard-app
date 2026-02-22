from django import forms
from .models import ClientProfile

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['name', 'email', 'address', 'contact_person']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Company Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'client@example.com'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500', 'rows': 3, 'placeholder': 'Client Address'}),
            'contact_person': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Contact Person Name'}),
        }
