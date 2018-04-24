from django.shortcuts import render, get_object_or_404

from subscribe.models import Tag, Subscriber
from utils.functions import normalize_email


def register(request):
    context = {}

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')

        email = normalize_email(email)

        if not nickname or not email:
            context['nickname'] = nickname
            context['email'] = email
            context['error_message'] = 'Nickname and email are required fields.'
        else:
            subscriber, _ = Subscriber.objects.get_or_create(email=email)
            subscriber.nickname = nickname
            subscriber.save()

            context['subscriber'] = subscriber

    return render(request, 'register.html', context)


def subscribe(request, token):
    subscriber = get_object_or_404(Subscriber, token=token)
    context = {
        'tags': list(Tag.objects.all()),
        'subscriber': subscriber,
    }

    if request.method == 'POST':
        selected_tags = [
            tag
            for tag in Tag.objects.all()
            if str(tag.id) in request.POST
        ]
        subscriber.subscribed_tags.set(selected_tags, clear=True)

        context['success'] = True

    context['subscribed_tags'] = list(subscriber.subscribed_tags.all())

    return render(request, 'subscribe.html', context)
