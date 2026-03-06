from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    logo = models.ImageField(
        upload_to='site/', blank=True, null=True,
        verbose_name='Логотип'
    )
    phone = models.CharField(
        max_length=30, default='+380 00 000 00 00',
        verbose_name='Телефон'
    )
    email = models.EmailField(
        default='info@example.com',
        verbose_name='Email'
    )
    address = models.CharField(
        max_length=255, blank=True,
        verbose_name='Адреса офісу'
    )
    telegram_url = models.URLField(blank=True, verbose_name='Telegram')
    viber_url = models.URLField(blank=True, verbose_name='Viber')
    whatsapp_url = models.URLField(blank=True, verbose_name='WhatsApp')
    call_btn_text = models.CharField(
        max_length=60, default='Замовити башту',
        verbose_name='Текст кнопки дзвінка'
    )

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return 'Налаштування сайту'


class HeroSection(SingletonModel):
    title = models.CharField(
        max_length=120, default='ВОДОНАПІРНІ БАШТИ РОЖНОВСЬКОГО — ВІД ВИРОБНИКА',
        verbose_name='Заголовок'
    )
    subtitle = models.TextField(
        default='Виготовляємо сталеві водонапірні башти 15, 25, 50 м³. Монтаж під ключ, доставка по всій Україні. Гарантія та сертифікати.',
        verbose_name='Підзаголовок'
    )
    btn_buy_text = models.CharField(
        max_length=60, default='ЗАМОВИТИ БАШТУ',
        verbose_name='Кнопка «Купити»'
    )
    btn_sell_text = models.CharField(
        max_length=60, default='ОТРИМАТИ КОНСУЛЬТАЦІЮ',
        verbose_name='Кнопка «Продати»'
    )
    bg_image = models.ImageField(
        upload_to='hero/', blank=True, null=True,
        verbose_name='Фонове зображення'
    )
    overlay_opacity = models.FloatField(
        default=0.65,
        verbose_name='Прозорість фільтра (0–1)'
    )

    class Meta:
        verbose_name = 'Hero-секція'
        verbose_name_plural = 'Hero-секція'

    def __str__(self):
        return 'Hero-секція'


class AboutSection(SingletonModel):
    title = models.CharField(
        max_length=120, default='Про підприємство',
        verbose_name='Заголовок секції'
    )
    philosophy_title = models.CharField(
        max_length=160,
        default='Надійний виробник башт Рожновського з 20-річним досвідом',
        verbose_name='Заголовок філософії'
    )
    philosophy_text = models.TextField(
        verbose_name='Текст філософії'
    )

    class Meta:
        verbose_name = 'Секція «Про компанію»'
        verbose_name_plural = 'Секція «Про компанію»'

    def __str__(self):
        return 'Про компанію'


class ProductionSection(SingletonModel):
    title = models.CharField(
        max_length=120, default='Наші можливості',
        verbose_name='Заголовок секції'
    )
    platform_title = models.CharField(
        max_length=120, default='Сертифіковане виробництво',
        verbose_name='Заголовок платформи'
    )
    platform_text = models.TextField(verbose_name='Опис платформи')
    seller_title = models.CharField(
        max_length=80, default='Для промислових об\'єктів',
        verbose_name='Заголовок блоку продавця'
    )
    seller_text = models.TextField(verbose_name='Текст для продавця')
    buyer_title = models.CharField(
        max_length=80, default='Для громад та агросектору',
        verbose_name='Заголовок блоку покупця'
    )
    buyer_text = models.TextField(verbose_name='Текст для покупця')
    important_note = models.TextField(
        verbose_name='Важлива примітка (виноска)'
    )

    class Meta:
        verbose_name = 'Секція «Наші можливості»'
        verbose_name_plural = 'Секція «Наші можливості»'

    def __str__(self):
        return 'Наші можливості'


class ServiceItem(models.Model):
    CATEGORY_CHOICES = [
        ('buyer', 'Основна продукція'),
        ('seller', 'Додаткові послуги'),
    ]
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES,
        verbose_name='Категорія'
    )
    title = models.CharField(max_length=120, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Опис')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['category', 'order']
        verbose_name = 'Послуга'
        verbose_name_plural = 'Наші послуги'

    def __str__(self):
        return f'{self.get_category_display()} — {self.title}'
