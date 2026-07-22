from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from category.models import Category

from .models import Article


class AdminLanguageAndSlugTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="स्थानीय समाचार")
        self.user = get_user_model().objects.create_superuser(
            username="admin-test",
            email="admin@example.com",
            password="test-password",
        )

    def test_hindi_and_english_titles_generate_unique_slugs(self):
        hindi = Article.objects.create(
            title="चंदौली में नई सड़क योजना",
            summary="Summary",
            content="Content",
            category=self.category,
        )
        english = Article.objects.create(
            title="English News Title",
            summary="Summary",
            content="Content",
            category=self.category,
        )
        duplicate = Article.objects.create(
            title="English News Title",
            summary="Summary",
            content="Content",
            category=self.category,
        )

        self.assertEqual(hindi.slug, "चंदौली-में-नई-सड़क-योजना")
        self.assertTrue(any("\u0900" <= char <= "\u097f" for char in hindi.slug))
        self.assertEqual(english.slug, "english-news-title")
        self.assertEqual(duplicate.slug, "english-news-title-2")

    def test_admin_is_english_and_slug_prepopulation_allows_unicode(self):
        self.client.force_login(self.user)
        response = self.client.get("/admin/news/article/add/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add article")
        self.assertContains(response, "Save and add another")
        self.assertIn('&quot;allowUnicode&quot;: true', html)
        self.assertContains(response, "/static/admin/js/unicode_slugify.js")

    def test_admin_accepts_complete_hindi_slug(self):
        self.client.force_login(self.user)
        response = self.client.post(
            "/admin/news/article/add/",
            {
                "title": "मुख्यमंत्री योगी आदित्यनाथ ने किए मां पाटेश्वरी के दर्शन",
                "slug": "मुख्यमंत्री-योगी-आदित्यनाथ-ने-किए-मां-पाटेश्वरी-के-दर्शन",
                "summary": "",
                "content": "पूरी खबर",
                "category": self.category.pk,
                "status": "published",
                "_save": "Save",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
            response.context["adminform"].form.errors.as_json() if response.status_code == 200 else "",
        )
        self.assertTrue(
            Article.objects.filter(
                slug="मुख्यमंत्री-योगी-आदित्यनाथ-ने-किए-मां-पाटेश्वरी-के-दर्शन"
            ).exists()
        )

    def test_public_site_remains_hindi(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ताज़ा खबरें")

    def test_latest_uploaded_article_appears_first(self):
        older = Article.objects.create(
            title="Older uploaded article",
            summary="",
            content="Content",
            category=self.category,
            status="published",
        )
        newer = Article.objects.create(
            title="Latest uploaded article",
            summary="",
            content="Content",
            category=self.category,
            status="published",
        )

        self.assertEqual(Article.objects.first(), newer)
        response = self.client.get("/")
        latest_articles = list(response.context["latest"])
        self.assertEqual(latest_articles[:2], [newer, older])

    def test_article_has_social_links_and_complete_metadata(self):
        article = Article.objects.create(
            title="सोशल मीडिया टेस्ट खबर",
            summary="शेयर करते समय दिखाई देने वाला सारांश",
            content="पूरी खबर",
            category=self.category,
            status="published",
        )
        response = self.client.get(article.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'property="og:type" content="article"')
        self.assertContains(response, 'property="og:image:width" content="1200"')
        self.assertContains(response, 'property="og:image:height" content="630"')
        self.assertContains(response, 'name="twitter:card" content="summary_large_image"')
        self.assertContains(response, "https://wa.me/")
        self.assertContains(response, "facebook.com/sharer/sharer.php")
        self.assertContains(response, "twitter.com/intent/tweet")
        self.assertContains(response, "t.me/share/url")
        self.assertContains(response, 'id="copy-share-link"')
        self.assertContains(response, f"/s/{article.pk}/")
        self.assertContains(response, f"/social/article/{article.pk}.jpg")
        self.assertEqual(response.context["share_url"], f"http://testserver/s/{article.pk}/")

    def test_social_thumbnail_is_always_1200_by_630_jpeg(self):
        article = Article.objects.create(
            title="बिना फोटो की खबर",
            summary="",
            content="पूरी खबर",
            category=self.category,
            status="published",
        )
        response = self.client.get(f"/social/article/{article.pk}.jpg")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "image/jpeg")
        image = Image.open(BytesIO(response.content))
        self.assertEqual(image.size, (1200, 630))

    def test_short_ascii_share_url_renders_the_article(self):
        article = Article.objects.create(
            title="लंबे हिंदी यूआरएल वाली खबर",
            summary="सारांश",
            content="पूरी खबर",
            category=self.category,
            status="published",
        )
        response = self.client.get(f"/s/{article.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.title)
        self.assertContains(response, f'property="og:url" content="http://testserver/s/{article.pk}/"')
        self.assertContains(response, f'rel="canonical" href="http://testserver{article.get_absolute_url()}"')
