from django.shortcuts import render

def TGSitePage(request):
    return render(request, 'template-parts/TargetSite.html')


def TGS_HistoryPage(request):
    return render(request, 'template-parts/history.html')

def TGS_GraphPage(request):
    return render(request, 'template-parts/graph-charts.html')