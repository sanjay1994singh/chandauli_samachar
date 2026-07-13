from category.models import Category
def navigation(request): return {"nav_categories": Category.objects.filter(is_active=True)[:8]}
