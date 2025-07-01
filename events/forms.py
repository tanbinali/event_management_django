from django import forms
from .models import Event, Category, Participant

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm',
                'rows': 4
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
            'location': forms.TextInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
            'category': forms.Select(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm',
                'rows': 4
            }),
        }

        
        
class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
            }),
            'events': forms.CheckboxSelectMultiple(attrs={
                'class': 'ml-2 space-y-1'
            }),
        }


