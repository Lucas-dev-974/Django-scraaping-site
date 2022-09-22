from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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