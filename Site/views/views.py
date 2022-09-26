from django.shortcuts import render

# Create your views here.
def Home(request):
    scraps = [
        {
            'site name': 'Site a scrapper 1',
            'title': 'Thread 1',
            'state': 'success',
            'content': '15 letters max of the post (thread) content'
        },
        {
            'site name': 'Site a scrapper 1',
            'title': 'Thread 2',
            'state': 'success',
            'content': '15 letters max of the post (thread) content'
        },
    ]
    return render(request, 'template-parts/home.html', {
        'last_scraps': scraps
    }) 

