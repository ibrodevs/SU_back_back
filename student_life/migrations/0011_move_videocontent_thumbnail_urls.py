from django.db import migrations


def move_thumbnail_urls(apps, schema_editor):
    VideoContent = apps.get_model("student_life", "VideoContent")

    for video in VideoContent.objects.filter(thumbnail__startswith="http"):
        thumbnail_str = str(video.thumbnail or "")
        update_fields = {"thumbnail": ""}

        if not video.thumbnail_url:
            update_fields["thumbnail_url"] = thumbnail_str

        VideoContent.objects.filter(pk=video.pk).update(**update_fields)


class Migration(migrations.Migration):

    dependencies = [
        ("student_life", "0010_alter_videocontent_thumbnail_url"),
    ]

    operations = [
        migrations.RunPython(move_thumbnail_urls, migrations.RunPython.noop),
    ]
