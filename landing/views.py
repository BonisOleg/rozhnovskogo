import logging
from types import SimpleNamespace

from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

from .models1 import SiteSettings, HeroSection, AboutSection, ProductionSection, ServiceItem
from .models2 import (
    WorkStep, StatItem, AdvantageItem, AdvantagesSection,
    ServicesSection, ContactSection, LeadSubmission,
)
from .keyword_groups import detect_group, get_translation


def _to_ns(obj):
    """Recursively convert dicts to SimpleNamespace so templates access via dot notation."""
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: _to_ns(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [_to_ns(i) for i in obj]
    return obj


def _get_context():
    return {
        'site': SiteSettings.load(),
        'hero': HeroSection.load(),
        'about': AboutSection.load(),
        'auction': ProductionSection.load(),
        'services_section': ServicesSection.load(),
        'service_items': ServiceItem.objects.all(),
        'steps': WorkStep.objects.all(),
        'stats': StatItem.objects.all(),
        'advantages_section': AdvantagesSection.load(),
        'advantages': AdvantageItem.objects.all(),
        'contact': ContactSection.load(),
    }


_OVERRIDABLE_KEYS = [
    'hero', 'about', 'services_section', 'service_items',
    'steps', 'stats', 'advantages_section', 'advantages', 'contact',
]


def _apply_translation(ctx, kw_param):
    group_id = detect_group(kw_param)
    translation = get_translation(group_id)
    ctx['t'] = translation['t']
    ctx['lang'] = translation['lang']
    for key in _OVERRIDABLE_KEYS:
        if key in translation:
            ctx[key] = _to_ns(translation[key])


class IndexView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(_get_context())
        kw_param = self.request.GET.get('kw', '').strip()
        _apply_translation(ctx, kw_param)
        return ctx


class LeadFormView(View):
    def post(self, request):
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        interest = request.POST.get('interest', 'buy')
        lang = request.POST.get('lang', 'uk')

        if name and phone:
            LeadSubmission.objects.create(name=name, phone=phone, interest=interest)

        contact = ContactSection.load()
        return render(request, 'landing/htmx/lead_success.html', {
            'contact': contact,
            'lang': lang,
        })
