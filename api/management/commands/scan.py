from django.core.management.base import BaseCommand
from api.models import User
from api.directory_watcher import scan_photos
from api.util import logger
import uuid

class Command(BaseCommand):
    help = 'scan directory for all users'

    def add_arguments(self, parser):
        parser.add_argument('--full-scan', action='store_true',
            help=("Perform a full scan of all files "
                  "(including already scanned files which haven't changed since last scan)")
        )

    def handle(self, *args, full_scan=False, **kwargs):
        for user in User.objects.all():
            scan_photos(user, full_scan, uuid.uuid4())
