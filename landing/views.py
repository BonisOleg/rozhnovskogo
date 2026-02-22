import logging
import time

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


def _get_context():
    return {
        'site': SiteSettings.load(),
        'hero': HeroSection.load(),
        'about': AboutSection.load(),
        'auction': AuctionSection.load(),
        'services_section': ServicesSection.load(),
        'service_buyers': ServiceItem.objects.filter(category='buyer'),
        'service_sellers': ServiceItem.objects.filter(category='seller'),
        'steps': WorkStep.objects.all(),
        'stats': StatItem.objects.all(),
        'advantages_section': AdvantagesSection.load(),
        'advantages': AdvantageItem.objects.all(),
        'contact': ContactSection.load(),
    }


class IndexView(TemplateView):
    template_name = 'landing/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(_get_context())
        return ctx


class LeadFormView(View):
    def post(self, request):
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        interest = request.POST.get('interest', 'buy')

        if name and phone:
            LeadSubmission.objects.create(name=name, phone=phone, interest=interest)

        contact = ContactSection.load()
        return render(request, 'landing/htmx/lead_success.html', {'contact': contact})


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
                items = data.get('data') or data.get('results') or data.get('items') or []
                if not items and data.keys() - {'data', 'results', 'items'}:
                    logger.warning(
                        'Prozorro API response structure may have changed: keys=%s',
                        list(data.keys()),
                    )
                result = []
                for item in items[:6]:
                    result.append({
                        'id': item.get('id', ''),
                        'title': item.get('title', 'Земельна ділянка'),
                        'area': self._extract_area(item),
                        'price': self._extract_price(item),
                        'status': item.get('status', ''),
                        'url': f"https://prozorro.sale/auction/{item.get('id', '')}",
                        'region': self._extract_region(item),
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
            unit = item['items'][0].get('unit', {}).get('name', 'га')
            return f'{qty} {unit}'
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
            return item['items'][0]['deliveryAddress'].get('region', '')
        except (KeyError, IndexError, TypeError):
            return ''
