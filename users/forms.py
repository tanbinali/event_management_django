from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tailwind_input_classes = (
            "block w-full border border-gray-300 bg-white text-gray-900 "
            "rounded px-3 py-2 shadow-sm "
            "focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
        )
        for field in self.fields.values():
            field.widget.attrs.update({'class': tailwind_input_classes})
            field.help_text = None

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        if commit:
            user.save()
        return user

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        tailwind_input_classes = (
            "block w-full border border-gray-300 bg-white text-gray-900 "
            "rounded px-3 py-2 shadow-sm "
            "focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
        )

        for field in self.fields.values():
            field.widget.attrs.update({'class': tailwind_input_classes})
            field.help_text = None