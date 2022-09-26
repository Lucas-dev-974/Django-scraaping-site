import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Site.Formulaires import *
from Site.models import Target_Site
from Site.Formulaires import *

@login_required
def private(request):   
    errors = []
    if request.method == 'POST':
        form = ModelTargetSiteForm(request.POST)
        if(form.is_valid()):
            form.save()

        # Manage errors from formulaire"
        else:
            errors_asjson     = form.errors.as_json()
            errors_jsonloaded = json.loads(errors_asjson)
            for error in errors_jsonloaded:
                if len(errors_jsonloaded) > 1:
                    print('plusieur erreur')
                else:
                    error_msg = errors_jsonloaded[error][0]['message']
                    errors.append(error_msg)

        
    else:
        form = ModelTargetSiteForm()

    return render(request, 'template-parts/private.html', {'add_TGSite_form': form, 'notif': {
        'on': len(errors) > 0,
        'type': 'warning',
        'messages': errors
    }})


@login_required
def TGSite(request):
    #if request.method == 'POST':
    print('okok')
    return render(request, 'template-parts/TargetSite.html')

@login_required
def TGS_History(request):
    return render(request, 'template-parts/history.html')

@login_required 
def TGS_Graph(request):
    return render(request, 'template-parts/graph-charts.html')