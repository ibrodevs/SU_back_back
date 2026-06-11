from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student_life", "0009_eresourcecategory_eresource_eresourcefeature"),
    ]

    operations = [
        migrations.AlterField(
            model_name="videocontent",
            name="thumbnail_url",
            field=models.URLField(
                blank=True,
                help_text="Ссылка на внешнее превью (альтернатива загрузке файла)",
                max_length=500,
                null=True,
                verbose_name="URL превью",
            ),
        ),
    ]
