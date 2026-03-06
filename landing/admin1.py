from django.contrib import admin
from django.utils.html import format_html
from .models1 import SiteSettings, HeroSection, AboutSection, ProductionSection, ServiceItem


class SingletonAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    fieldsets = (
        ('Логотип та контакти', {
            'fields': ('logo', 'logo_preview', 'phone', 'email', 'address'),
        }),
        ('Месенджери', {
            'fields': ('telegram_url', 'viber_url', 'whatsapp_url'),
        }),
        ('Кнопки', {
            'fields': ('call_btn_text',),
        }),
    )
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:4px;" />',
                obj.logo.url
            )
        return '—'
    logo_preview.short_description = 'Попередній перегляд'


@admin.register(HeroSection)
class HeroSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Тексти', {
            'fields': ('title', 'subtitle', 'btn_buy_text', 'btn_sell_text'),
        }),
        ('Фон', {
            'fields': ('bg_image', 'bg_preview', 'overlay_opacity'),
        }),
    )
    readonly_fields = ('bg_preview',)

    def bg_preview(self, obj):
        if obj.bg_image:
            return format_html(
                '<img src="{}" style="max-width:400px;max-height:160px;'
                'object-fit:cover;border-radius:6px;" />',
                obj.bg_image.url
            )
        return '—'
    bg_preview.short_description = 'Попередній перегляд'


@admin.register(AboutSection)
class AboutSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Секція «Про компанію»', {
            'fields': ('title', 'philosophy_title', 'philosophy_text'),
        }),
    )


@admin.register(ProductionSection)
class ProductionSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Загальне', {
            'fields': ('title', 'platform_title', 'platform_text'),
        }),
        ('Для продавця', {
            'fields': ('seller_title', 'seller_text'),
        }),
        ('Для покупця', {
            'fields': ('buyer_title', 'buyer_text'),
        }),
        ('Важлива примітка', {
            'fields': ('important_note',),
        }),
    )


@admin.register(ServiceItem)
class ServiceItemAdmin(admin.ModelAdmin):
    list_display = ('category', 'title', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    ordering = ('category', 'order')
