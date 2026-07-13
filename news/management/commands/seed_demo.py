from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from category.models import Category
from state_city.models import State, City
from news.models import Article
from advertisements.models import Advertisement
class Command(BaseCommand):
    help = "Create polished demo content"
    def handle(self, *args, **kwargs):
        state, _ = State.objects.get_or_create(name="उत्तर प्रदेश", defaults={"slug":"uttar-pradesh"})
        cities = {n: City.objects.get_or_create(state=state, name=n, defaults={"slug":s})[0] for n,s in [("चंदौली","chandauli"),("मुगलसराय","mughalsarai"),("सकलडीहा","sakaldiha")]}
        cats = {n: Category.objects.get_or_create(name=n, defaults={"slug":s,"order":i})[0] for i,(n,s) in enumerate([("चंदौली","chandauli"),("उत्तर प्रदेश","uttar-pradesh"),("राजनीति","politics"),("अपराध","crime"),("शिक्षा","education"),("खेल","sports"),("व्यापार","business")])}
        rows = [
          ("चंदौली में विकास कार्यों को मिली नई रफ्तार, कई परियोजनाओं का हुआ शुभारंभ","चंदौली","चंदौली","जिले में सड़क, स्वास्थ्य और शिक्षा से जुड़ी नई परियोजनाओं का शुभारंभ किया गया।","https://images.unsplash.com/photo-1594736797933-d0501ba2fe65?auto=format&fit=crop&w=1200&q=80"),
          ("किसानों के लिए आधुनिक कृषि प्रशिक्षण शिविर आयोजित","व्यापार","सकलडीहा","कृषि विशेषज्ञों ने किसानों को उन्नत बीज और नई तकनीक की जानकारी दी।","https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=80"),
          ("विद्यालयों में शुरू हुआ विशेष नामांकन अभियान","शिक्षा","चंदौली","बच्चों को गुणवत्तापूर्ण शिक्षा से जोड़ने के लिए जिलेभर में अभियान चलाया जा रहा है।","https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=80"),
          ("युवा खिलाड़ियों ने जिला स्तरीय प्रतियोगिता में दिखाया दम","खेल","मुगलसराय","प्रतियोगिता में ग्रामीण क्षेत्रों से आए खिलाड़ियों ने शानदार प्रदर्शन किया।","https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=1200&q=80"),
          ("नगर में यातायात व्यवस्था सुधारने को नया प्लान तैयार","चंदौली","मुगलसराय","प्रमुख चौराहों पर ट्रैफिक प्रबंधन और पार्किंग व्यवस्था को बेहतर बनाया जाएगा।","https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?auto=format&fit=crop&w=1200&q=80"),
          ("जनसुनवाई में जिलाधिकारी ने सुनीं लोगों की समस्याएं","उत्तर प्रदेश","चंदौली","अधिकारियों को शिकायतों के समयबद्ध और पारदर्शी निस्तारण के निर्देश दिए गए।","https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1200&q=80"),
        ]
        for i,(title,cat,city,summary,img) in enumerate(rows):
            slug = f"demo-news-{i+1}"
            Article.objects.update_or_create(slug=slug, defaults={"title":title,"summary":summary,"content":summary+"\n\nकार्यक्रम में स्थानीय नागरिकों, अधिकारियों और जनप्रतिनिधियों ने भाग लिया। संबंधित विभाग ने कहा कि योजनाओं का लाभ अंतिम व्यक्ति तक पहुंचाना प्राथमिकता है।\n\nचंदौली समाचार इस खबर से जुड़े हर नए अपडेट को आप तक पहुंचाता रहेगा।","category":cats[cat],"state":state,"city":cities[city],"status":"published","published_at":timezone.now(),"image_url":img,"is_featured":i==0,"is_breaking":i in (0,1)})
        Advertisement.objects.update_or_create(name="The Up Media Services - News Portal", defaults={"advertiser":"The Up Media Services", "headline":"अपना न्यूज़ पोर्टल बनवाएं", "subheadline":"24 घंटे में गूगल पर होगा रैंक", "contact":"8279408396", "whatsapp":"6397712918", "cta_text":"Call Now", "placement":"home_sidebar", "style":"creative", "priority":100, "is_active":True})
        self.stdout.write(self.style.SUCCESS("Demo categories, locations, articles and advertisement created."))
