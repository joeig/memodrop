import sys

from django.core.management import BaseCommand

from braindump.models import CardPlacement
from categories.models import Category, ShareContract


class CheckResult:
    def __init__(self, category, ok, nok):
        self.category = category
        self.ok = ok
        self.nok = nok


class Command(BaseCommand):
    help = 'Checks the consistency of card placements'

    def add_arguments(self, parser):
        """Argument handle
        """
        parser.add_argument('--repair', help='Try to repair inconsistencies', action='store_true')

    def handle(self, *args, **options):
        """Command handle
        """
        self.stdout.write('')
        self.stdout.write('----------------------------------------')
        self.stdout.write('Checking card placements for category owners')
        check_category_owners = self._check_category_owners()
        self._format_category_results(check_category_owners)

        self.stdout.write('')
        self.stdout.write('----------------------------------------')
        self.stdout.write('Checking card placements for users of shared categories')
        check_category_users = self._check_category_users()
        self._format_category_results(check_category_users)

        if options['repair']:
            self.stdout.write('')
            self.stdout.write('----------------------------------------')
            self.stdout.write('Trying to fix the inconsistencies')
            for result in check_category_owners + check_category_users:
                for nok in result.nok:
                    card_placement = CardPlacement.objects.create(
                        card=nok[0],
                        user=nok[1],
                    )
                    self.stdout.write(self.style.SUCCESS('Created %s for result %s' % (card_placement, nok)))
        else:
            self.stdout.write('')
            inconsistency_detected = False
            for result in check_category_owners + check_category_users:
                if result.nok:
                    inconsistency_detected = True
                    self.stdout.write('Try to fix the inconsistencies with --repair')
                    break

            if inconsistency_detected:
                sys.exit(1)

    def _format_category_results(self, results):
        """Print formatted category results
        """
        for result in results:
            self.stdout.write('#%d %s' % (result.category.id, result.category))
            self.stdout.write(self.style.SUCCESS('  - %dx OK' % len(result.ok)))
            for nok in result.nok:
                self.stdout.write(self.style.ERROR('  - Missing card placement: {}'.format(nok)))

    def _check_category_owners(self):
        """Iterates through all categories and checks its owners
        """
        resp = list()
        for category in Category.objects.all():
            ok, nok = self._check_card_placement(category, category.owner)
            resp.append(CheckResult(category, ok, nok))
        return resp

    def _check_category_users(self):
        """Iterates through all share contracts and checks its users
        """
        resp = list()
        for share_contract in ShareContract.objects.all():
            ok, nok = self._check_card_placement(share_contract.category, share_contract.user)
            resp.append(CheckResult(share_contract.category, ok, nok))
        return resp

    def _check_card_placement(self, category, user):
        """Iterates through all cards and looks for card placements
        """
        ok = list()
        nok = list()
        for card in category.cards.all():
            if CardPlacement.objects.filter(card=card, user=user).exists():
                ok.append((card, user))
            else:
                nok.append((card, user))
        return ok, nok
