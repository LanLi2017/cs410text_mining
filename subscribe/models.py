from django.db import models
from django.urls import reverse

from utils.functions import random_token


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    nickname = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    subscribed_tags = models.ManyToManyField(Tag, blank=True)
    token = models.CharField(unique=True, max_length=100, default=random_token)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.nickname:
            return '{} <>'.format(self.nickname, self.email)
        else:
            return self.email

    def subscribe_page_url(self):
        return reverse('subscribe:subscribe', kwargs={'token': self.token})
