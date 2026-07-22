from io import BytesIO
from urllib.parse import urlencode

from PIL import Image, ImageOps
from django.conf import settings
from django.db.models import F, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import Truncator

from .models import Article


def home(request):
    qs = Article.objects.filter(status="published").select_related("category", "city")
    return render(request, "news/home.html", {"featured": qs.filter(is_featured=True).first() or qs.first(), "latest": qs.order_by("-created_at", "-pk")[:9], "breaking": qs.filter(is_breaking=True).order_by("-created_at", "-pk")[:6]})


def _render_article(request, article):
    Article.objects.filter(pk=article.pk).update(views=F("views") + 1)
    article.refresh_from_db(fields=["views"])
    related = Article.objects.filter(status="published", category=article.category).exclude(pk=article.pk)[:4]
    canonical_url = request.build_absolute_uri(article.get_absolute_url())
    share_url = request.build_absolute_uri(reverse("article_share", args=[article.pk]))
    share_image_url = request.build_absolute_uri(reverse("article_social_image", args=[article.pk]))
    share_image_url = f"{share_image_url}?v={int(article.updated_at.timestamp())}"
    share_description = article.summary.strip() or Truncator(strip_tags(article.content)).chars(180)
    share_text = f"{article.title}\n{share_url}"
    return render(request, "news/detail.html", {
        "article": article,
        "related": related,
        "canonical_url": canonical_url,
        "share_url": share_url,
        "share_image_url": share_image_url,
        "share_description": share_description,
        "whatsapp_share_url": "https://wa.me/?" + urlencode({"text": share_text}),
        "facebook_share_url": "https://www.facebook.com/sharer/sharer.php?" + urlencode({"u": share_url}),
        "x_share_url": "https://twitter.com/intent/tweet?" + urlencode({"url": share_url, "text": article.title}),
        "telegram_share_url": "https://t.me/share/url?" + urlencode({"url": share_url, "text": article.title}),
    })


def article_detail(request, slug):
    article = get_object_or_404(Article.objects.select_related("category", "author", "city"), slug=slug, status="published")
    return _render_article(request, article)


def article_share(request, pk):
    article = get_object_or_404(
        Article.objects.select_related("category", "author", "city"),
        pk=pk,
        status="published",
    )
    return _render_article(request, article)


def article_social_image(request, pk):
    article = get_object_or_404(Article, pk=pk, status="published")
    fallback_path = settings.BASE_DIR / "static" / "img" / "social-default.jpg"

    try:
        if article.featured_image:
            article.featured_image.open("rb")
            source = Image.open(article.featured_image).convert("RGB")
        else:
            source = Image.open(fallback_path).convert("RGB")
        social_image = ImageOps.fit(source, (1200, 630), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    except (OSError, ValueError):
        social_image = Image.open(fallback_path).convert("RGB")

    output = BytesIO()
    social_image.save(output, format="JPEG", quality=88, optimize=True, progressive=True)
    response = HttpResponse(output.getvalue(), content_type="image/jpeg")
    response["Cache-Control"] = "public, max-age=3600"
    response["Content-Disposition"] = f'inline; filename="article-{article.pk}-social.jpg"'
    return response
def category_articles(request, slug):
    qs = Article.objects.filter(status="published", category__slug=slug).select_related("category", "city").order_by("-created_at", "-pk")
    return render(request, "news/list.html", {"articles": qs, "heading": get_object_or_404(__import__('category.models', fromlist=['Category']).Category, slug=slug).name})
def search(request):
    q = request.GET.get("q", "").strip(); qs = Article.objects.filter(status="published").order_by("-created_at", "-pk")
    if q: qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q) | Q(content__icontains=q))
    return render(request, "news/list.html", {"articles": qs, "heading": f"खोज: {q}", "query": q})
