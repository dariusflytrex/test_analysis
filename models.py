from __future__ import unicode_literals

import json
from enum import Enum
from django.db import models
from django.core import serializers


class Status(Enum):
    WaitingForDeliveryInitiation = 0
    WaitingToBeMounted = 1
    Mounted = 2
    Inflight = 3
    BeingReleased = 4
    Delivered = 5
    # aborted for some reason, on the way back to storage house. Will be changed back to WaitingToBeDelivered on arrival
    Aborted = 99

class Circle(models.Model):

    test_name = models.CharField(
        max_length=128,
        verbose_name="Pull address"
    )

    test_time = models.FloatField(
        verbose_name="Test time"
    )

    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Circle"

    def __str__(self):
        return "Circle"

class Webhook(models.Model):

    pull_address = models.CharField(
        max_length=128,
        verbose_name="Pull address"
    )

    sha_number = models.CharField(
        max_length=128,
        verbose_name="Sha number"
    )

    def __unicode__(self):
        return "Webhook"

    def __str__(self):
        return "Webhook"

class Package(models.Model):

    tracking_number = models.CharField(
        max_length=32,
        verbose_name="Tracking number"
    )

    name = models.CharField(
        max_length=128,
        verbose_name="Customer's name"
    )

    storage = models.CharField(
        max_length=128,
        verbose_name = "Warehouse Storage Location"
    )

    weight_kg = models.FloatField(
        verbose_name="Weight of packages in kg"
    )

    mobile = models.CharField(
        max_length=16,
        verbose_name="mobile phone number of the recipient"
    )

    status = models.IntegerField(
        default=Status.WaitingForDeliveryInitiation.value,
        verbose_name="Package Status"
    )

    class Meta:
        # Make Package unique per center/tracking_number values together
        unique_together = ('status', 'tracking_number')

    def __unicode__(self):
        return "Package"

    def __str__(self):
        return "Package"

    # @classmethod
    # def create(cls, **details):
    #     """
    #     :param details: Dictionary contains new center data
    #     :return: New model object
    #     """
    #     # Get package center
    #     if isinstance(details['center'], dict):
    #         details['center'] = Center.objects.get(organization__title=details['center']['organization']['title'],
    #                                                name=details['center']['name'])
    #
    #     # Create model class from dictionary
    #     return cls(**details)
    #
    # def save(self, *args, **kwargs):
    #     """
    #     Override model save and added model validation as part of the save() processing. Raises IntegrityError in case
    #     of model validation data error
    #     """
    #     # Validate model fields
    #     self.full_clean()
    #
    #     # Save model
    #     super(Package, self).save(*args, **kwargs)
    #
    # @property
    # def data(self):
    #     data = json.loads(serializers.serialize('json', [self, ]))[0]["fields"]
    #     data["center"] = self.center.data
    #     data["id"] = self.id
    #     return data
    #
    # @property
    # def _status(self):
    #     """
    #     Used to transform status from int to string.
    #     2 steps:
    #     1. change int to Status class instance, and take name
    #     2. change CamelCaps to space separated name. e.g HelloWorld => Hello World
    #     :return: name of status
    #     """
    #     return ''.join(map(lambda x: x if x.islower() else " "+x, Status(self.status).name))
