from django.db import models
from .models1 import SingletonModel


class WorkStep(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name='Номер кроку')
    title = models.CharField(max_length=160, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Опис')
    is_highlighted = models.BooleanField(
        default=False,
        verbose_name='Виділити золотим (Крок 4)'
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Крок роботи'
        verbose_name_plural = 'Як ми працюємо (кроки)'

    def __str__(self):
        return f'Крок {self.number}: {self.title}'


class StatItem(models.Model):
    value = models.CharField(max_length=40, verbose_name='Значення')
    label = models.CharField(max_length=120, verbose_name='Підпис')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика (цифри)'

    def __str__(self):
        return f'{self.value} — {self.label}'


ICON_CHOICES = [
    ('shield', 'Щит (безпека)'),
    ('chart', 'Графік (вигода)'),
    ('clock', 'Годинник (досвід)'),
    ('key', 'Ключ (під ключ)'),
    ('eye', 'Око (моніторинг)'),
    ('checkmark', 'Галочка (гарантія)'),
    ('star', 'Зірка'),
    ('map', 'Карта'),
]


class AdvantageItem(models.Model):
    icon_key = models.CharField(
        max_length=20, choices=ICON_CHOICES, default='shield',
        verbose_name='Іконка'
    )
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Опис')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Перевага'
        verbose_name_plural = 'Переваги'

    def __str__(self):
        return self.title


class AdvantagesSection(SingletonModel):
    title = models.CharField(
        max_length=120,
        default='Чому обирають наші башти Рожновського?',
        verbose_name='Заголовок секції'
    )
    subtitle = models.CharField(
        max_length=200,
        default='Власне виробництво, монтаж під ключ та ціни без посередників по всій Україні.',
        verbose_name='Підзаголовок'
    )
    footer_quote = models.TextField(
        default=(
            'Від розрахунку до здачі об\'єкту — ми беремо на себе все. '
            'Доставка та монтаж башт Рожновського у будь-який куточок України.'
        ),
        verbose_name='Цитата внизу блоку'
    )

    class Meta:
        verbose_name = 'Секція «Переваги»'
        verbose_name_plural = 'Секція «Переваги»'

    def __str__(self):
        return 'Переваги'


class ServicesSection(SingletonModel):
    title = models.CharField(
        max_length=120, default='Наша продукція та послуги',
        verbose_name='Заголовок секції'
    )
    steps_title = models.CharField(
        max_length=160,
        default='Як ми працюємо: від замовлення до запуску',
        verbose_name='Заголовок блоку кроків'
    )

    class Meta:
        verbose_name = 'Секція «Послуги»'
        verbose_name_plural = 'Секція «Послуги»'

    def __str__(self):
        return 'Послуги'


class ContactSection(SingletonModel):
    title = models.CharField(
        max_length=120,
        default='Замовити башту Рожновського',
        verbose_name='Заголовок'
    )
    description = models.TextField(
        default='Наші фахівці розрахують вартість башти, підберуть оптимальний об\'єм та нададуть консультацію щодо монтажу.',
        verbose_name='Опис'
    )
    form_title = models.CharField(
        max_length=120,
        default='Залишити заявку на розрахунок',
        verbose_name='Заголовок форми'
    )
    form_btn_text = models.CharField(
        max_length=80,
        default='ОТРИМАТИ ПРОПОЗИЦІЮ',
        verbose_name='Текст кнопки форми'
    )
    privacy_note = models.CharField(
        max_length=200,
        default='Ми гарантуємо конфіденційність вашого звернення та оперативну відповідь.',
        verbose_name='Приміт. конфіденційності'
    )

    class Meta:
        verbose_name = 'Секція «Контакти»'
        verbose_name_plural = 'Секція «Контакти»'

    def __str__(self):
        return 'Контакти'


class LeadSubmission(models.Model):
    INTEREST_CHOICES = [
        ('buy', 'Водонапірні башти'),
        ('sell', 'Котли та опалення'),
        ('estimate', 'Металоконструкції'),
    ]
    name = models.CharField(max_length=120, verbose_name="Ім'я")
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    interest = models.CharField(
        max_length=10, choices=INTEREST_CHOICES,
        verbose_name='Запит'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    is_processed = models.BooleanField(
        default=False, verbose_name='Оброблено'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.name} ({self.phone}) — {self.get_interest_display()}'
