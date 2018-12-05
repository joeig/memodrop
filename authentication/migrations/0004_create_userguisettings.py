from django.db import migrations


def create_userguisettings(apps, schema_editor):
    """Creates UserGuiSettings items for existing users
    """
    User = apps.get_model('auth', 'User')
    UserGUISettings = apps.get_model('authentication', 'UserGUISettings')

    UserGUISettings.objects.bulk_create(
        UserGUISettings(user=user)
        for user in User.objects.all()
    )


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0003_auto_20181203_1431'),
    ]

    operations = [
        migrations.RunPython(create_userguisettings, migrations.RunPython.noop),
    ]
