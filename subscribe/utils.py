import csv

from subscribe.models import Subscriber


def dump_data(file, queryset=None):
    if queryset is None:
        queryset = Subscriber.objects

    writer = csv.writer(file)
    writer.writerow([
        'nickname',
        'email',
        'subscribe_page_url',
        'create_date',
        'subscribed_tags',
    ])

    for subscriber in queryset.all():
        writer.writerow(
            [
                subscriber.nickname,
                subscriber.email,
                subscriber.subscribe_page_url(),
                subscriber.create_date,
                ' '.join(str(e) for e in (list(subscriber.subscribed_tags.all()))),
            ]
        )
