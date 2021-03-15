from mainapp.models import CreateRss

def get_rss(request):
    rss = CreateRss.objects.values_list('id','title', 'url')

    return {
        'datos':rss
    }