from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from Site.Formulaires import *
from Site.models import Target_Site
from Site.Formulaires import *
from Site.utils import *

@login_required
def private(request):   
    errors = []
    if request.method == 'POST':
        if 'add_tgsite' in request.POST:
            form = ModelTargetSiteForm(request.POST)
            if(form.is_valid()):
                form.save()
            # Manage errors from formulaire"
            else:
                errors += checkFormError(form=form)     

        
    else:
        form = ModelTargetSiteForm()

    target_sites = Target_Site.objects.all()
    paginator    = Paginator(target_sites, 10)

    if 'page' in request.GET:
        on_page = request.GET.get('page')
    else: on_page = 0

    tgsites_page = paginator.get_page(on_page)
    #paginator = request.get.page

    return render(request, 'template-parts/private.html', {
        'add_TGSite_form': form, 
        'notif': {
            'on': len(errors) > 0,
            'type': 'warning',
            'messages': errors
        },
        'tgsites': tgsites_page
    })


@login_required
def TGSite(request):
    #if request.method == 'POST':
    print('okok')
    return render(request, 'template-parts/TargetSite.html')

@login_required
def TGS_History(request):
    scrapHist = [
        {
            'date': '10/05/1990',
            'nbTh': '1',
            'state': 'success',
            'nbCom': '15'
        },
        {
            'date': '01/01/2000',
            'nbTh': '10',
            'state': 'success',
            'nbCom': '50'
        },
    ]
    return render(request, 'template-parts/history.html', {
        'scrap_history': scrapHist
    })

@login_required 
def TGS_Graph(request):
    return render(request, 'template-parts/graph-charts.html')