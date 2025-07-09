from django import forms
from .models import Event, Category
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import User
from .models import Event, Category
from django.forms.widgets import FileInput


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['rsvps','participants'] 
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
            'image': FileInput(attrs={
                'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm',
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
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'
        }),
        required=False,
        label='Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'}),
            'email': forms.EmailInput(attrs={'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'}),
            'first_name': forms.TextInput(attrs={'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'bg-gray-100 border border-gray-300 rounded w-full px-4 py-2 shadow-sm'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            from django.contrib.auth.models import Group
            group, created = Group.objects.get_or_create(name='Participant')
            user.groups.add(group)
        return user
