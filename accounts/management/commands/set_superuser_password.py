from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Sets password for existing superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username='admin')
            user.set_password('()@#560jose')
            user.save()
            self.stdout.write(self.style.SUCCESS('Password set for superuser "admin".'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Superuser "admin" does not exist.'))
