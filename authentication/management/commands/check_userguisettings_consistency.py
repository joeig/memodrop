import sys

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from authentication.models import UserGUISettings


class Command(BaseCommand):
    help = 'Checks the consistency of user specific GUI settings'

    def add_arguments(self, parser):
        """Argument handle
        """
        parser.add_argument('--repair', help='Try to repair inconsistencies', action='store_true')

    def handle(self, *args, **options):
        """Command handle
        """
        users = User.objects.all()
        users_ok = list()
        users_nok = list()
        for user in users:
            user_gui_settings_item = UserGUISettings.objects.filter(user=user)
            if user_gui_settings_item.exists():
                users_ok.append(user)
            else:
                users_nok.append(user)

        for user in users_ok:
            self.stdout.write(self.style.SUCCESS('%s OK' % user))
        for user in users_nok:
            self.stdout.write(self.style.ERROR('%s NOT OK' % user))

        if options['repair']:
            self.stdout.write('')
            self.stdout.write('Trying to fix the inconsistencies')
            for user in users_nok:
                user_gui_settings_item = UserGUISettings(user=user)
                user_gui_settings_item.save()
                self.stdout.write(self.style.SUCCESS('Created #%d for user %s' % (user_gui_settings_item.id, user)))
        else:
            if users_nok:
                self.stdout.write('')
                self.stdout.write('Try to fix the inconsistencies with --repair')
                sys.exit(1)
