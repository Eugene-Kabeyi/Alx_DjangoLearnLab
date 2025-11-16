from django.contrib.auth.models import Group, Permission
from django.apps import apps

def setup_groups():
    Document = apps.get_model('secure_app', 'Document')

    perms = Permission.objects.filter(content_type__app_label='secure_app')

    viewers = Group.objects.get_or_create(name='Viewers')[0]
    viewers.permissions.set(perms.filter(codename='can_view'))

    editors = Group.objects.get_or_create(name='Editors')[0]
    editors.permissions.set(perms.filter(codename__in=['can_view', 'can_create', 'can_edit']))

    admins = Group.objects.get_or_create(name='Admins')[0]
    admins.permissions.set(perms)

    print("Groups configured successfully!")
