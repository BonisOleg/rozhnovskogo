from django.core.management.base import BaseCommand
from landing.models1 import SiteSettings, HeroSection, AboutSection, ProductionSection, ServiceItem
from landing.models2 import (
    WorkStep, StatItem, AdvantageItem, AdvantagesSection,
    ServicesSection, ContactSection,
)


class Command(BaseCommand):
    help = 'Seed database with Ukrkotlobud landing page content'

    def handle(self, *args, **options):
        self._seed_site()
        self._seed_hero()
        self._seed_about()
        self._seed_auction()
        self._seed_services()
        self._seed_steps()
        self._seed_stats()
        self._seed_advantages()
        self._seed_contact()
        self.stdout.write(self.style.SUCCESS('Seed completed successfully.'))

    def _seed_site(self):
        obj = SiteSettings.load()
        obj.phone = '+380 (68) 833-47-92'
        obj.email = 'marina.ukrkotlobud@ukr.net'
        obj.address = 'Черкаська обл., смт Маньківка, вул. Малиновського, 1-Б'
        obj.call_btn_text = 'Замовити башту'
        obj.save()

    def _seed_hero(self):
        obj = HeroSection.load()
        obj.title = 'ВОДОНАПІРНІ БАШТИ РОЖНОВСЬКОГО — ВІД ВИРОБНИКА'
        obj.subtitle = (
            'Виготовляємо сталеві водонапірні башти об\'ємом 15, 25 та 50 м³. '
            'Монтаж під ключ, доставка та введення в експлуатацію по всій Україні. '
            'Гарантія та повна технічна документація.'
        )
        obj.btn_buy_text = 'ЗАМОВИТИ БАШТУ'
        obj.btn_sell_text = 'ОТРИМАТИ КОНСУЛЬТАЦІЮ'
        obj.overlay_opacity = 0.70
        obj.save()

    def _seed_about(self):
        obj = AboutSection.load()
        obj.title = 'Про підприємство'
        obj.philosophy_title = 'Надійний виробник башт Рожновського з 20-річним досвідом'
        obj.philosophy_text = (
            'ПП «Укркотлобуд» — виробник водонапірних башт Рожновського типових об\'ємів 15, 25 та 50 м³. '
            'Виготовляємо башти за типовими та індивідуальними проектами з якісної сталі. '
            'Здійснюємо доставку, будівництво фундаменту та монтаж під ключ по всій Україні. '
            'Уся продукція сертифікована, ціни — безпосередньо від виробника без посередників.'
        )
        obj.save()

    def _seed_auction(self):
        obj = ProductionSection.load()
        obj.title = 'Наші можливості'
        obj.platform_title = 'Виробництво та монтаж під ключ'
        obj.platform_text = (
            'Ми забезпечуємо повний цикл: від виготовлення башти на власному виробництві '
            'до здачі об\'єкта в експлуатацію. Будівництво фундаменту, монтаж, підключення до мережі — '
            'все включено. Жодних прихованих доплат.'
        )
        obj.seller_title = 'Для промислових підприємств'
        obj.seller_text = (
            'Башти Рожновського 15, 25, 50 м³ для виробничих потреб.\n'
            'Індивідуальні проекти будь-якого об\'єму.\n'
            'Монтаж на існуючий або новий фундамент.'
        )
        obj.buyer_title = 'Для сіл, громад та агросектору'
        obj.buyer_text = (
            'Централізоване водопостачання для сільських громад.\n'
            'Водозабезпечення ферм та агропідприємств.\n'
            'Розрахунок, погодження проекту та здача «під ключ».'
        )
        obj.important_note = (
            'Для бюджетних установ та органів місцевого самоврядування можлива '
            'оплата після прийому об\'єкту в експлуатацію.'
        )
        obj.save()

    def _seed_services(self):
        ServicesSection.objects.update_or_create(pk=1, defaults={
            'title': 'Наша продукція та послуги',
            'steps_title': 'Як ми працюємо: від замовлення до запуску',
        })
        ServiceItem.objects.all().delete()

        prods = [
            ('Водонапірні башти Рожновського', 'Виготовлення башт 15, 25, 50 м³ зі сталі. Типові та індивідуальні проекти. Гарантія від виробника.'),
            ('Монтаж башт під ключ', 'Будівництво фундаменту, монтаж башти, підключення до мережі водопостачання та введення в експлуатацію.'),
            ('Парові котли КОВС-«Е»', 'Котли від 100 до 2000 кг пари на годину на твердому, рідкому паливі або газі.'),
            ('Водогрійні котли НІІСТУ-5', 'Котли будь-яких розмірів, монтаж та обмурування. Повна технічна документація.'),
        ]
        extra = [
            ('Металоконструкції', 'Виготовлення ферм, ангарів, бункерів та ресиверів будь-якої складності.'),
            ('Печі Булер\'ян', '7 видів опалювальних печей для різних об\'ємів приміщень.'),
            ('Демонтаж старих башт', 'Безпечний демонтаж застарілих водонапірних башт та котлів по всій Україні.'),
            ('Сервіс та документація', 'Надання повного пакету дозвільної та технічної документації на всі роботи.'),
        ]
        for i, (t, d) in enumerate(prods):
            ServiceItem.objects.create(category='buyer', title=t, description=d, order=i)
        for i, (t, d) in enumerate(extra):
            ServiceItem.objects.create(category='seller', title=t, description=d, order=i)

    def _seed_steps(self):
        WorkStep.objects.all().delete()
        steps = [
            (1, 'Консультація та розрахунок',
             'Обговорення потреб: об\'єм башти, висота, тип фундаменту. Безкоштовний розрахунок вартості.', False),
            (2, 'Договір та проектування',
             'Узгодження технічних характеристик, підписання договору та підготовка проектної документації.', False),
            (3, 'Виготовлення башти',
             'Виробництво башти на власному заводі з якісної сталі зі строгим контролем якості.', False),
            (4, 'Доставка та монтаж',
             'Доставка башти на об\'єкт, будівництво фундаменту та професійний монтаж під ключ.', True),
            (5, 'Здача та документація',
             'Підключення до мережі, пусконалагоджувальні роботи, передача повного пакету документів.', False),
        ]
        for num, title, desc, highlighted in steps:
            WorkStep.objects.create(
                number=num, title=title, description=desc,
                is_highlighted=highlighted, order=num
            )

    def _seed_stats(self):
        StatItem.objects.all().delete()
        items = [
            ('20+ років', 'Досвіду виробництва', 0),
            ('1000+', 'Встановлених башт', 1),
            ('500+', 'Виконаних монтажів', 2),
            ('100%', 'Сертифікована продукція', 3),
        ]
        for val, lbl, order in items:
            StatItem.objects.create(value=val, label=lbl, order=order)

    def _seed_advantages(self):
        obj = AdvantagesSection.load()
        obj.title = 'Чому обирають наші башти Рожновського?'
        obj.subtitle = 'Власне виробництво, монтаж під ключ та ціни без посередників по всій Україні.'
        obj.footer_quote = (
            'Від розрахунку до здачі об\'єкту — ми беремо на себе все. '
            'Доставка та монтаж башт Рожновського у будь-який куточок України.'
        )
        obj.save()

        AdvantageItem.objects.all().delete()
        items = [
            ('checkmark', 'Власне виробництво',
             'Виготовляємо башти самостійно — жодних посередників. Ціна напряму від заводу.', 0),
            ('key', 'Монтаж під ключ',
             'Фундамент, монтаж, підключення до мережі та введення в експлуатацію — все включено.', 1),
            ('chart', 'Ціни від виробника',
             'Без торговельних надбавок. Гнучкі умови оплати, у тому числі для бюджетних установ.', 2),
            ('shield', 'Гарантія та сертифікати',
             'Уся продукція сертифікована. Надаємо паспорт башти та технічну документацію.', 3),
            ('clock', 'Терміни від 10 днів',
             'Виготовлення стандартної башти Рожновського займає 10–20 робочих днів.', 4),
            ('map', 'Доставка по всій Україні',
             'Власна спецтехніка та логістичні партнери. Доставляємо та монтуємо по всій країні.', 5),
        ]
        for icon_key, title, desc, order in items:
            AdvantageItem.objects.create(
                icon_key=icon_key, title=title, description=desc, order=order
            )

    def _seed_contact(self):
        obj = ContactSection.load()
        obj.title = 'Замовити башту Рожновського'
        obj.description = (
            'Наші фахівці розрахують вартість башти, підберуть оптимальний об\'єм '
            'та нададуть консультацію щодо монтажу. Зв\'яжіться з нами зараз.'
        )
        obj.form_title = 'Залишити заявку на розрахунок'
        obj.form_btn_text = 'ОТРИМАТИ ПРОПОЗИЦІЮ'
        obj.privacy_note = (
            'Ми гарантуємо конфіденційність вашого звернення та оперативну відповідь.'
        )
        obj.save()
