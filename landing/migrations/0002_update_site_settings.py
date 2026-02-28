from django.db import migrations

def update_site_settings(apps, schema_editor):
    SiteSettings = apps.get_model('landing', 'SiteSettings')
    obj, _ = SiteSettings.objects.get_or_create(pk=1)
    obj.phone = '063 252 8901'
    obj.email = 'tsr.tsr0110@gmail.com'
    obj.address = 'м. Київ вулиця Анни Ахматової 7/15 офіс 1'
    obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_site_settings),
    ]
