from django import forms
from . models import DummyUser

class DummyUserForm(forms.ModelForm):
    class Meta:
        model = DummyUser
        fields = ('Email', 'Password')
    
    def __init__(self, *args, **kwargs) -> None:
        super(DummyUserForm, self).__init__(*args, **kwargs)

        self.fields['Email'].widget.attrs['class'] = 'form-control'
        self.fields['Password'].widget.attrs['class'] = 'form-control'