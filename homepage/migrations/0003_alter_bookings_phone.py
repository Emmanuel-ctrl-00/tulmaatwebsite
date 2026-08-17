from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_bookings_options_alter_rooms_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='Phone',
            field=models.CharField(max_length=20),
        ),
    ]
