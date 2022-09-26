import os
from django.shortcuts import render
from Site.Formulaires import *
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout, login
# from Site.CustomAuthentication import HashedPasswordAuthBackend
# Create your views here.

def Login(request):
    errors = []
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username = username, password = password)
            
            if user is not None:
                login(request=request, user=user)
                return redirect('/private', {'user': user})
            else:
                errors.append('Vos idientifiant sont incorrectes !')
        else:
            errors = login_form.errors.as_json()
    else:
        login_form = LoginForm()

    return render(request, 'template-parts/login.html', {'login_form': login_form, 'notif': {
        'on': len(errors) > 0,
        'type': 'warning',
        'messages': errors
    }})

def Register(request):
    errors  = {}
    user    = {}

    # If form is submited 
    if request.method == 'POST':

        # Create register form with the request POST params
        register_form = RegisterForm(request.POST)
        
        # Check if given params corelate with the form User model validation 
        if register_form.is_valid():

            # Create user with the form cleaned data
            _user = register_form.save()
            user['email']    = _user.email
            user['username'] = _user.username
            
            # Redirect to home page 
            return redirect('/', {'user': user})
        else:
            errors = register_form.errors.as_json()
    else:
        register_form = RegisterForm()
    
    # Ici on retourne une réponse HTTP avec le paramètre form qui vas nous permettre d'afficher les champs requis pour notre formulaire
    return render(request, 'template-parts/register.html', {'register_form': register_form, 'errors': errors, 'user': user})


def Logout(request):
    logout(request)
    return redirect('/', {
        'notif': {
            'on': True,
            'type': 'info',
            'message': 'Vous avez été déconnecter avec succès'
        }
    })