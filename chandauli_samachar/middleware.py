from django.utils import translation


class AdminEnglishMiddleware:
    """Use English in Django admin without changing the Hindi public website."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        previous_language = translation.get_language()
        if request.path.startswith("/admin/"):
            translation.activate("en")
            request.LANGUAGE_CODE = "en"

        try:
            return self.get_response(request)
        finally:
            translation.activate(previous_language)
