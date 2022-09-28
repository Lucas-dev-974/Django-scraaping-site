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
    form = ModelTargetSiteForm()

    if request.method == 'POST':
        if 'add_tgsite' in request.POST:
            form = ModelTargetSiteForm(request.POST)
            if(form.is_valid()):
                form.save()
            # Manage errors from formulaire"
            else:
                errors += checkFormError(form=form)     

        if 'delete_tgsite' in request.POST:
            tgsite_id = request.POST.get('tgsite_id') 
            try:
                tgsite_id = int(tgsite_id)
                tg_site = Target_Site.objects.get(pk = tgsite_id)
                tg_site.delete()
            except:
                print('error l\'id n\'est pas au bon format')
            print('delete site: ', request.POST.get('tgsite_id'))

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
def TGSite(request, id):
    threads = Threads.objects.filter(target_id_id = id)
    tg_site = Target_Site.objects.get(pk=id)

    iteration = 0

    for thread in threads:
        thread
        # threads[iteration]['replys'] = thread.replys()

        iteration += 1
        # thread['replys'] = thread.replys()

    return render(request, 'template-parts/TargetSite.html', {
        'site_name': tg_site.name,
        'site_url_to_scrapp':  tg_site.url_to_scrapp
    })



@login_required
def TGS_History(request):
    last_scrapped_threads = Threads.objects.all().order_by('scrapped_date')
    threads = []

    for thread in last_scrapped_threads:
        threads.append({
            'id': thread.id,
            'author': thread.author,
            'title': thread.title,
            'publication_date': thread.publication_date,
            'scrapped_date': thread.scrapped_date,
            'replys': thread.replys(),
            'number_of_replys': len(thread.replys()),
            'status': 'success'
        })


    return render(request, 'template-parts/history.html', {
        'scrap_history': threads,
    })

@login_required 
def TGS_Graph(request):
    return render(request, 'template-parts/graph-charts.html')


@login_required
def Releve(request, siteid):
    site = Target_Site.objects.get(pk = siteid)

    return render(request, 'template-parts/scrap.html', {
        'site': {
            'id': site.id,
            'name': site.name,
            'url_to_scrapp': site.url_to_scrapp
        }
    })