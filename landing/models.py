import string
from random import choice

from django.db import models


class UserRegistered(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    token = models.CharField(max_length=6)

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = self.get_token()

            while(UserRegistered.objects.filter(token=self.token).exists()):
                self.token = self.get_token()

        super(UserRegistered, self).save(*args, **kwargs)

    def get_token(self):
        chars = string.ascii_letters + string.digits
        token = ''.join(choice(chars) for i in range(6))

        return token


class Mail(models.Model):
    subject = models.CharField(max_length=255)
    to = models.CharField(max_length=255)
    from_email = models.EmailField()
    template = models.CharField(max_length=255)
    data = models.TextField()
    sent = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, blank=True)
    reject_reason = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.to


class Scenario(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='scenarios')
    subtitle = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='speakers')
    scenario = models.ForeignKey(Scenario)

    def __unicode__(self):
        return self.name
