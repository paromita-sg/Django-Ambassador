from django.core.management import BaseCommand
from django_redis import get_redis_connection

from faker import Faker
from core.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        con = get_redis_connection("default")
        ambassadors = User.objects.filter(is_ambassador=True)

        for a in ambassadors:
            con.zadd('rankings', {a.name: float(a.revenue)})
