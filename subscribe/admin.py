from django.contrib import admin
from django.http import HttpResponse

from subscribe.models import Tag, Subscriber
from subscribe.utils import dump_data


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'id',
        'name',
        'create_date',
    )
    list_filter = (
        'create_date',
    )
    readonly_fields = (
        'id',
        'create_date',
    )
    search_fields = (
        'name',
    )


def dump_subscribers_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    dump_data(response, queryset)

    return response


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    actions = [
        dump_subscribers_to_csv,
    ]
    fields = (
        'id',
        'nickname',
        'email',
        'subscribed_tags',
        'token',
        'subscribe_page_url',
        'create_date',
    )
    filter_horizontal = (
        'subscribed_tags',
    )
    list_display = (
        'nickname',
        'email',
    )
    list_filter = (
        'create_date',
    )
    readonly_fields = (
        'id',
        'subscribe_page_url',
        'create_date',
    )
    search_fields = (
        'nickname',
        'email',
    )
