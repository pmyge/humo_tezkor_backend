from django.core.management.base import BaseCommand
from users.models import UserProfile
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates or updates the punyo superuser'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'punyo'
        password = 'punyo33'
        
        user, created = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser "{username}"'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated superuser "{username}"'))
