from django.contrib import admin
from .admin1 import SingletonAdmin
from .models2 import (
    WorkStep, StatItem, AdvantageItem, AdvantagesSection,
    ServicesSection, ContactSection, LeadSubmission,
)


@admin.register(WorkStep)
class WorkStepAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'is_highlighted', 'order')
    list_editable = ('order', 'is_highlighted')
    ordering = ('order',)


@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(AdvantageItem)
class AdvantageItemAdmin(admin.ModelAdmin):
    list_display = ('icon_key', 'title', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(AdvantagesSection)
class AdvantagesSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Секція «Переваги»', {
            'fields': ('title', 'subtitle', 'footer_quote'),
        }),
    )


@admin.register(ServicesSection)
class ServicesSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Секція «Послуги»', {
            'fields': ('title', 'steps_title'),
        }),
    )


@admin.register(ContactSection)
class ContactSectionAdmin(SingletonAdmin):
    fieldsets = (
        ('Секція «Контакти»', {
            'fields': ('title', 'description', 'form_title', 'form_btn_text', 'privacy_note'),
        }),
    )


@admin.register(LeadSubmission)
class LeadSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'interest', 'created_at', 'is_processed')
    list_filter = ('interest', 'is_processed')
    list_editable = ('is_processed',)
    readonly_fields = ('name', 'phone', 'interest', 'created_at')
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False
