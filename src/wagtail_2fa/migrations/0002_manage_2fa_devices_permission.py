from django.db import migrations


def create_manage_devices_permission(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')

    wagtail_2fa_content_type, created = ContentType.objects.get_or_create(
        app_label='wagtail_2fa',
        model='wagtail2fa'
    )

    # A narrower permission than the stock change_user permission: lets a
    # user manage OTHER users' 2FA devices without granting general
    # user-editing rights (email, groups, is_superuser, is_active, etc).
    manage_devices_permission, created = Permission.objects.get_or_create(
        content_type=wagtail_2fa_content_type,
        codename='manage_2fa_devices',
        name='Can manage 2FA devices for other users'
    )


def remove_manage_devices_permission(apps, schema_editor):
    """Reverse the above addition of the permission."""
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    wagtail_2fa_content_type = ContentType.objects.get(
        app_label='wagtail_2fa',
        model='wagtail2fa',
    )

    # This also removes the permission from all groups
    Permission.objects.filter(
        content_type=wagtail_2fa_content_type,
        codename='manage_2fa_devices',
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('wagtail_2fa', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_manage_devices_permission, remove_manage_devices_permission),
    ]
