from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import ContactMessageForm

class AboutView(TemplateView): template_name = "pages/about.html"
class PrivacyView(TemplateView): template_name = "pages/privacy.html"
class DisclaimerView(TemplateView): template_name = "pages/disclaimer.html"
class TermsView(TemplateView): template_name = "pages/terms.html"
class EditorialPolicyView(TemplateView): template_name = "pages/editorial_policy.html"
class CorrectionPolicyView(TemplateView): template_name = "pages/correction_policy.html"

def contact(request):
    form = ContactMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "आपका संदेश प्राप्त हो गया है। हमारी टीम जल्द संपर्क करेगी।")
        return redirect("contact")
    return render(request, "pages/contact.html", {"form": form})
