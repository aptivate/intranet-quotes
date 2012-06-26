# extensions to django.core.context_processors

def additions(request):
    from models import Quote

    return {
        'quotes': {
            'latest': Quote.latest,
        },
    }
