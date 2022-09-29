from django.shortcuts import render

from Site.models import Target_Site, Threads

# Create your views here.
def Home(request):
    last_scraps = Threads.objects.all().order_by('scrapped_date')[:10]
    scraps      = []
    
    for scrap in last_scraps:
        scraps.append({
            'author': scrap.author,
            'publication_date': scrap.publication_date,
            'scrapped_date': scrap.scrapped_date,
            'total_replys': scrap.totalReplys(),
            'content': scrap.content,
            'site': scrap.target_id,
            'status': 'success'
        }) 
    return render(request, 'template-parts/home.html', {
        'last_scraps': scraps
    }) 

