from django.core.management.base import BaseCommand
from landing.models1 import SiteSettings, HeroSection, AboutSection, AuctionSection, ServiceItem
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
        obj.call_btn_text = 'Зв\'язатися з нами'
        obj.save()

    def _seed_hero(self):
        obj = HeroSection.load()
        obj.title = 'ПП «УКРКОТЛОБУД» — ВАШ НАДІЙНИЙ ПАРТНЕР У СФЕРІ ОПАЛЕННЯ'
        obj.subtitle = 'Виробництво промислових котлів, водонапірних башт Рожновського та металоконструкцій будь-якої складності. Якість, перевірена часом.'
        obj.btn_buy_text = 'КАТАЛОГ ПРОДУКЦІЇ'
        obj.btn_sell_text = 'ОТРИМАТИ КОНСУЛЬТАЦІЮ'
        obj.overlay_opacity = 0.75
        obj.save()

    def _seed_about(self):
        obj = AboutSection.load()
        obj.title = 'Про підприємство'
        obj.philosophy_title = 'Надійність, якість та індивідуальний підхід'
        obj.philosophy_text = (
            'Приватне підприємство «Укркотлобуд» спеціалізується на виробництві промислового опалювального обладнання. '
            'Ми виготовляємо водонапірні башти Рожновського за типовими та індивідуальними проектами, парові та водогрійні котли, '
            'а також металоконструкції будь-яких розмірів. Уся наша продукція сертифікована, а ціни — від виробника.'
        )
        obj.save()

    def _seed_auction(self):
        obj = AuctionSection.load()
        obj.title = 'Наші можливості'
        obj.platform_title = 'Сертифіковане виробництво'
        obj.platform_text = (
            'Ми забезпечуємо повний цикл робіт: від проектування та виготовлення до монтажу та сервісного обслуговування. '
            'Використовуємо сучасні технології та високоякісні матеріали для забезпечення довговічності нашого обладнання.'
        )
        obj.seller_title = 'Для промислових об\'єктів'
        obj.seller_text = (
            'Потужні парові котли (до 2000 кг пари/год).\n'
            'Водогрійні котли НІІСТУ-5.\n'
            'Транспортабельні котельні установки.'
        )
        obj.buyer_title = 'Для громад та агросектору'
        obj.buyer_text = (
            'Водонапірні башти Рожновського (15-50 м³).\n'
            'Будівництво фундаментів «під ключ».\n'
            'Демонтаж та монтаж обладнання.'
        )
        obj.important_note = (
            'Для бюджетних та державних установ можлива післяоплата за товар та виконані роботи.'
        )
        obj.save()

    def _seed_services(self):
        ServicesSection.objects.update_or_create(pk=1, defaults={
            'title': 'Наша продукція',
            'steps_title': 'Як ми працюємо: від замовлення до запуску',
        })
        ServiceItem.objects.all().delete()
        
        prods = [
            ('Водонапірні башти', 'Виготовлення башт Рожновського 15, 25, 50 м³, монтаж та підключення.'),
            ('Парові котли', 'Котли КОВС-«Е» від 100 до 2000 кг пари на годину на різних видах палива.'),
            ('Водогрійні котли', 'Котли НІІСТУ-5 будь-яких розмірів, монтаж та обмурування.'),
            ('Металоконструкції', 'Виготовлення ферм, ангарів, бункерів та ресиверів будь-якої складності.'),
        ]
        extra = [
            ('Печі Булер\'ян', '7 видів опалювальних печей для різних об\'ємів приміщень.'),
            ('Допоміжне обладнання', 'Димососи, вентилятори, циклони, чавунні колосники та димові труби.'),
            ('Монтажні роботи', 'Демонтаж старих та монтаж нових котлів і башт по всій Україні.'),
            ('Сервіс', 'Надання повної дозвільної та технічної документації на всі роботи.'),
        ]
        for i, (t, d) in enumerate(prods):
            ServiceItem.objects.create(category='buyer', title=t, description=d, order=i)
        for i, (t, d) in enumerate(extra):
            ServiceItem.objects.create(category='seller', title=t, description=d, order=i)

    def _seed_steps(self):
        WorkStep.objects.all().delete()
        steps = [
            (1, 'Консультація',
             'Обговорення потреб замовника, вибір оптимального обладнання або розробка індивідуального проекту.', False),
            (2, 'Договір та проектування',
             'Узгодження технічних характеристик, підписання договору та підготовка проектної документації.', False),
            (3, 'Виробництво',
             'Виготовлення обладнання на власних потужностях з суворим контролем якості на кожному етапі.', False),
            (4, 'Доставка та монтаж',
             'Транспортування обладнання на об\'єкт, професійний монтаж та підключення до мереж.', True),
            (5, 'Запуск та сервіс',
             'Пусконалагоджувальні роботи, надання документації та подальше гарантійне обслуговування.', False),
        ]
        for num, title, desc, highlighted in steps:
            WorkStep.objects.create(
                number=num, title=title, description=desc,
                is_highlighted=highlighted, order=num
            )

    def _seed_stats(self):
        StatItem.objects.all().delete()
        items = [
            ('20+ років', 'Досвіду на ринку', 0),
            ('1000+', 'Виготовлених башт', 1),
            ('500+', 'Встановлених котлів', 2),
            ('100%', 'Сертифікована продукція', 3),
        ]
        for val, lbl, order in items:
            StatItem.objects.create(value=val, label=lbl, order=order)

    def _seed_advantages(self):
        obj = AdvantagesSection.load()
        obj.title = 'Чому обирають ПП «Укркотлобуд»?'
        obj.subtitle = 'Ми гарантуємо надійність нашого обладнання та високу якість виконання робіт.'
        obj.footer_quote = (
            'Ціни від виробника та повний спектр послуг — від проектування до монтажу по всій Україні.'
        )
        obj.save()

        AdvantageItem.objects.all().delete()
        items = [
            ('checkmark', 'Сертифікована якість',
             'Уся продукція має необхідні сертифікати відповідності та технічну документацію.', 0),
            ('key', 'Робота «під ключ»',
             'Ми беремо на себе все: від будівництва фундаменту до запуску обладнання.', 1),
            ('chart', 'Ціни виробника',
             'Ви отримуєте найкращу ціну без посередників та гнучкі умови оплати.', 2),
            ('shield', 'Надійність',
             'Наше обладнання розраховане на тривалу експлуатацію у складних умовах.', 3),
            ('clock', 'Багаторічний досвід',
             'Понад 20 років досвіду у виробництві промислового опалювального обладнання.', 4),
            ('map', 'Доставка по Україні',
             'Здійснюємо доставку та монтаж обладнання у будь-яку точку України.', 5),
        ]
        for icon_key, title, desc, order in items:
            AdvantageItem.objects.create(
                icon_key=icon_key, title=title, description=desc, order=order
            )

    def _seed_contact(self):
        obj = ContactSection.load()
        obj.title = 'Маєте запитання? Зв\'яжіться з нами!'
        obj.description = (
            'Наші фахівці допоможуть підібрати обладнання, розрахувати вартість та нададуть професійну консультацію.'
        )
        obj.form_title = 'Залишити заявку на розрахунок'
        obj.form_btn_text = 'ОТРИМАТИ ПРОПОЗИЦІЮ'
        obj.privacy_note = (
            'Ми гарантуємо конфіденційність вашого звернення та оперативну відповідь.'
        )
        obj.save()
