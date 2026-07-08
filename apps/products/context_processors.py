from .models import Category

def global_categories(request):
    """
    Context processor to make all categories available to all templates globally.
    Useful for populating the navbar dropdown.
    """
    return {
        'global_categories': Category.objects.all()
    }
