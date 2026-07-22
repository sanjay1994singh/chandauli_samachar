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
