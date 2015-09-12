from django.core.management.base import BaseCommand, CommandError

from app.models import BuyBackBike
from app.models import Transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        for bb in BuyBackBike.objects.all():
            self.stdout.write(str(bb.transaction.id))

            # rb.transaction = Transaction
            # rb.save()


            # trans = Transaction.objects
            # trans.save()
            # rb.transaction = trans
            # rb.save()
