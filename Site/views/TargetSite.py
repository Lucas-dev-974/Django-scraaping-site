from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Site.Formulaires import *
from Site.models import Target_Site


@login_required
def private(request):   
    if request.method == 'POST':
        form = ModelTargetSiteForm(request)

        print()
    else:
        form = ModelTargetSiteForm()
    print()

    return render(request, 'template-parts/private.html')


@login_required
def TGSite(request):
    print('okok')
    return render(request, 'template-parts/TargetSite.html')

@login_required
def TGS_History(request):
    return render(request, 'template-parts/history.html')

@login_required 
def TGS_Graph(request):
    return render(request, 'template-parts/graph-charts.html')