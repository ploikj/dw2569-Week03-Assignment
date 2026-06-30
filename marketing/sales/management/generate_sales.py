from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Generates sales data'

    def add_arguments(self, parser):
        # Add any arguments here
        # parser.add_argument('--amount', type=int, help='Amount of sales to generate')
        pass

    def handle(self, *args, **options):
        # Add your logic here
        # amount = options.get('amount')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully generated sales data!')
        )
