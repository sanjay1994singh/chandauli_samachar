from django import template
from django.db.models import Q
from django.utils import timezone
from advertisements.models import Advertisement
register = template.Library()
@register.inclusion_tag("advertisements/ad_slot.html")
def show_ad(placement="home_sidebar", size="wide"):
    now = timezone.now()
    ad = Advertisement.objects.filter(is_active=True, placement=placement).filter(Q(starts_at__isnull=True) | Q(starts_at__lte=now)).filter(Q(ends_at__isnull=True) | Q(ends_at__gte=now)).order_by("-priority", "?").first()
    return {"ad": ad, "size": size}
