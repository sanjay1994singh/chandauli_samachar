from django.db.models import F, Q
from django.shortcuts import get_object_or_404, render
from .models import Article
def home(request):
    qs = Article.objects.filter(status="published").select_related("category", "city")
    return render(request, "news/home.html", {"featured": qs.filter(is_featured=True).first() or qs.first(), "latest": qs.order_by("-created_at", "-pk")[:9], "breaking": qs.filter(is_breaking=True).order_by("-created_at", "-pk")[:6]})
def article_detail(request, slug):
    article = get_object_or_404(Article.objects.select_related("category", "author", "city"), slug=slug, status="published")
    Article.objects.filter(pk=article.pk).update(views=F("views") + 1); article.refresh_from_db(fields=["views"])
    related = Article.objects.filter(status="published", category=article.category).exclude(pk=article.pk)[:4]
    return render(request, "news/detail.html", {"article": article, "related": related})
def category_articles(request, slug):
    qs = Article.objects.filter(status="published", category__slug=slug).select_related("category", "city").order_by("-created_at", "-pk")
    return render(request, "news/list.html", {"articles": qs, "heading": get_object_or_404(__import__('category.models', fromlist=['Category']).Category, slug=slug).name})
def search(request):
    q = request.GET.get("q", "").strip(); qs = Article.objects.filter(status="published").order_by("-created_at", "-pk")
    if q: qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))
    return render(request, "news/list.html", {"articles": qs, "heading": f"खोज: {q}", "query": q})
