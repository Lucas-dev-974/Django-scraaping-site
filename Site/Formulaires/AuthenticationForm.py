from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    email    = forms.CharField(max_length=70, required=False)
    username = forms.CharField(max_length=70, )
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

    error_messages = {}

    # Overide
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Manage custom error here
        self.fields['username'].error_messages['unique'] = "Ce nom d'utilisateur est déjà pris"
        self.fields['email'].error_messages['invalid']   = "Veuillez entrer un mail valide"

    # Define form relation with database table
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        help_text = {
            'email': 'requis',
            'username': 'requis',
            'password': 'requis'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-input'
            }),
        }

    # Overide 
    def save(self):
        user = User.objects.create_user(
            email    = self.cleaned_data['email'], 
            username = self.cleaned_data['username'], 
            password = self.cleaned_data['password']
        )
        return user



class LoginForm(forms.Form):
    username = forms.CharField(label='Nom utilisateur', max_length=70, required=True)
    password = forms.CharField(label='Mot de passe', max_length=100, widget=forms.PasswordInput(), required=True)
    