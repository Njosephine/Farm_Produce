from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Set superuser password'

    def handle(self, *args, **kwargs):
        try:
            user = User.objects.get(username='admin')
            user.set_password('()@#560jose')
            user.save()
            self.stdout.write(self.style.SUCCESS('Superuser password has been set successfully!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User with username "admin" does not exist'))
