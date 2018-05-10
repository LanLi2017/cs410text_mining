from django.core.management.base import BaseCommand

from subscribe.utils import dump_data


class Command(BaseCommand):
    help = 'Dump all subscribers\' data'

    def add_arguments(self, parser):
        parser.add_argument(
            '-o', '--output-file',
            default='data.csv',
            dest='output_file',
            help='Output file name',
        )

    def handle(self, *args, **options):
        with open(
                options['output_file'], 'wt',
                encoding='utf-8', newline='',
        ) as f:
            dump_data(f)
