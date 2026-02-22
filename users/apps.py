from django.apps import AppConfig
from django.db.models.signals import post_migrate

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)

def create_groups(sender, **kwargs):
    from django.contrib.auth.models import Group
    groups = ['SuperAdmin', 'Admin', 'Manager', 'Technician']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
