from django.contrib.auth.models import User
from django.core.management import BaseCommand
#Introducir aqui el nuevo modelo de datos de usuario para que funcione


class Command(BaseCommand):
    help = 'creates a user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='alumnodb').exists():
            User.objects.create_superuser(
                username='alumnodb',
                password='alumnodb'
            )
            print("SuperUser created")
