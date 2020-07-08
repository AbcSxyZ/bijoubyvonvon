from stands.models import Stand
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Remove or update finished stands"

    def handle(self, *args, **kwargs):
        Stand.manage_stand()


