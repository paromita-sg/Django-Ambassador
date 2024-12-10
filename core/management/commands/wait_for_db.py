from django.core.management import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('waiting for the db ...')
        conn = True

        while not conn:
            try:
                conn = connections['default']
            except OperationalError:
                self.stdout.write('Db unavaiable, waiting for 1 sec ...')
                time.sleep()

        self.stdout.write(self.style.SUCCESS('DB available!!'))
