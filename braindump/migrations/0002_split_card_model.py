from django.db import migrations


def split_card_model(apps, schema_editor):
    """Splits attributes of Card into CardPlacement
    """
    Card = apps.get_model('cards', 'Card')
    CardPlacement = apps.get_model('braindump', 'CardPlacement')

    CardPlacement.objects.bulk_create(
        CardPlacement(area=old_object.area,
                      card=old_object,
                      user=old_object.category.owner,
                      last_interaction=old_object.last_interaction,
                      postpone_until=old_object.postpone_until)
        for old_object in Card.objects.all()
    )


class Migration(migrations.Migration):
    dependencies = [
        ('braindump', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(split_card_model, migrations.RunPython.noop),
    ]
