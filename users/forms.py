#кот пипсика весь
from django import forms
from .models import User

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль"
    )

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Пароль"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтвердите пароль"
    )
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'surname', 'phone_number']
    
    def clean(self):
        data = super().clean()
        if data['password'] != data['confirm_password']:
            raise forms.ValidationError("Пароли не совпадают!")
        return data