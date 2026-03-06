import logging
import time
from datetime import datetime
from types import SimpleNamespace

import requests
from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)

from .models1 import SiteSettings, HeroSection, AboutSection, AuctionSection, ServiceItem
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
        'auction': AuctionSection.load(),
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


class ProzorroView(View):
    CACHE_KEY = 'prozorro_land_auctions'
    CACHE_KEY_ERROR = 'prozorro_land_auctions_api_error'
    RETRIES = 3
    BACKOFF = 1.5
    TIMEOUT = getattr(settings, 'PROZORRO_API_TIMEOUT', 12)

    def get(self, request):
        cached = cache.get(self.CACHE_KEY)
        cached_error = cache.get(self.CACHE_KEY_ERROR)

        if cached is not None:
            return render(request, 'landing/htmx/prozorro_cards.html', {
                'auctions': cached,
                'api_error': cached_error or False,
            })

        auctions, api_error = self._fetch_auctions()
        cache.set(self.CACHE_KEY, auctions, settings.PROZORRO_CACHE_TIMEOUT)
        cache.set(self.CACHE_KEY_ERROR, api_error, settings.PROZORRO_CACHE_TIMEOUT)

        return render(request, 'landing/htmx/prozorro_cards.html', {
            'auctions': auctions,
            'api_error': api_error,
        })

    def _fetch_auctions(self):
        for attempt in range(self.RETRIES):
            try:
                resp = requests.get(
                    settings.PROZORRO_API_URL,
                    timeout=self.TIMEOUT,
                )
                resp.raise_for_status()
                data = resp.json()
                items = data if isinstance(data, list) else []
                
                active_items = [
                    item for item in items 
                    if item.get('status') == 'active_tendering'
                ]
                
                result = []
                for item in active_items[:6]:
                    result.append({
                        'id': item.get('auctionId', ''),
                        'title': item.get('title', {}).get('uk_UA', 'Земельна ділянка'),
                        'area': self._extract_area(item),
                        'price': self._extract_price(item),
                        'status': item.get('status', ''),
                        'url': f"https://prozorro.sale/auction/{item.get('auctionId', '')}/",
                        'region': self._extract_region(item),
                        'auction_start': self._extract_auction_start(item),
                    })
                return result, False
            except requests.RequestException as e:
                logger.warning(
                    'Prozorro API request failed (attempt %s/%s): %s: %s',
                    attempt + 1, self.RETRIES, type(e).__name__, str(e),
                )
                if attempt < self.RETRIES - 1:
                    time.sleep(self.BACKOFF * (attempt + 1))
                else:
                    logger.error('Prozorro API unreachable after %s attempts', self.RETRIES)
                    return [], True
            except (ValueError, KeyError, TypeError) as e:
                logger.exception('Prozorro API response parse error: %s', e)
                return [], True
        return [], True

    def _extract_area(self, item):
        try:
            qty = item['items'][0]['quantity']
            unit_name = item['items'][0].get('unit', {}).get('name', {})
            if isinstance(unit_name, dict):
                unit_text = unit_name.get('uk_UA', 'га')
            else:
                unit_text = str(unit_name) if unit_name else 'га'
            return f'{qty} {unit_text}'
        except (KeyError, IndexError, TypeError):
            return '—'

    def _extract_price(self, item):
        try:
            val = item['value']['amount']
            currency = item['value'].get('currency', 'UAH')
            return f'{val:,.0f} {currency}'
        except (KeyError, TypeError):
            return '—'

    def _extract_region(self, item):
        try:
            region = item['items'][0]['address'].get('region', {})
            if isinstance(region, dict):
                return region.get('uk_UA', '')
            return str(region) if region else ''
        except (KeyError, IndexError, TypeError):
            return ''

    def _extract_auction_start(self, item):
        try:
            start_date = item.get('auctionPeriod', {}).get('startDate', '')
            if start_date:
                dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                return dt.strftime('%d.%m.%Y %H:%M')
            return ''
        except (ValueError, TypeError, AttributeError):
            return ''
