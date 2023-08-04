from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs) -> None:
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        # Remove the help text for password1 and password2 fields
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class CustomPasswordChangeForm(PasswordChangeForm):
    # Modify field labels
    old_password = forms.CharField(label='Current Password')
    new_password1 = forms.CharField(label='New Password')
    new_password2 = forms.CharField(label='Confirm New Password')

    # Add custom help texts
    new_password1 = forms.CharField(
        label='New Password',
        help_text='Your new password must be at least 8 characters long.'
    )

    # Add custom validation
    def clean_new_password1(self):
        new_password1 = self.cleaned_data['new_password1']
        # Add your custom validation logic here, e.g., check for minimum length, complexity, etc.
        return new_password1
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].help_text = ''
        self.fields['new_password1'].help_text = ''
        self.fields['new_password2'].help_text = ''