from django.urls import path
from . import views
urlpatterns = [
    path("about-us/", views.AboutView.as_view(), name="about"),
    path("contact-us/", views.contact, name="contact"),
    path("privacy-policy/", views.PrivacyView.as_view(), name="privacy"),
    path("disclaimer/", views.DisclaimerView.as_view(), name="disclaimer"),
    path("terms-and-conditions/", views.TermsView.as_view(), name="terms"),
    path("editorial-policy/", views.EditorialPolicyView.as_view(), name="editorial_policy"),
    path("correction-policy/", views.CorrectionPolicyView.as_view(), name="correction_policy"),
]
