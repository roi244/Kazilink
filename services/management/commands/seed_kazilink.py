from django.core.management.base import BaseCommand

from services.models import ServiceCategory


class Command(BaseCommand):
    help = 'Initialize default KaziLink service categories.'

    def handle(self, *args, **options):
        categories = [
            ('Plomberie', 'Depannage et installation plomberie'),
            ('Electricite', 'Maintenance et installations electriques'),
            ('Climatisation', 'Reparation et entretien climatisation'),
        ]

        for name, description in categories:
            ServiceCategory.objects.get_or_create(name=name, defaults={'description': description})

        self.stdout.write(self.style.SUCCESS('Categories KaziLink initialisees.'))
