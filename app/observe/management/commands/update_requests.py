from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from datetime import datetime, timedelta
from observe.views import update_status
from observe.images import email_users
from observe.models import Observation

class Command(BaseCommand):
    help = 'Update pending blocks if observation requests have been made'

    def handle(self, *args, **options):
        updated_reqs = []
        requests = Observation.objects.filter(~Q(status='C'), ~Q(status='F'))
        self.stdout.write("==== %s Pending requests %s ====" % (requests.count(), datetime.now().strftime('%Y-%m-%d %H:%M')))
        for req in requests:
            self.stdout.write("Updating {}".format(req))
            status = update_status(req)
            if status:
                updated_reqs.append(req)
        if updated_reqs:
            email_users(updated_reqs)
