from django.db import models
from django.core.validators import MinValueValidator, MaxLengthValidator
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
from datetime import datetime

# Create your models here.


class Campaign(models.Model):
    """
    Model representing a campaign.
    """
    name = models.CharField(
        max_length=200,
        validators=[MaxLengthValidator(200)],
    )
    start_datetime = models.DateTimeField(
        default=datetime.now,
        verbose_name='Start Date & Time',
    )
    end_datetime = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='End Date & Time',
    )
    total_budget = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        help_text='Minimum $25',
        # validators will not be run automatically when you save a model,
        # but if you are using a ModelForm, it will run your validators on
        # any fields that are included in your form.
        validators=[MinValueValidator(25)],
    )
    daily_budget = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        help_text='Minimum $25',
        validators=[MinValueValidator(25)],
    )
    ACTIVE = 'AC'
    PAUSED = 'PA'
    DELETED = 'DE'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PAUSED, 'Paused'),
        (DELETED, 'Deleted'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PAUSED,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["update_date"]

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular campaign instance.
        """
        return reverse('campaign-detail', args=[str(self.id)])


class Strategy(models.Model):
    """
    Model representing a strategy.
    """
    campaign = models.ForeignKey(
        Campaign,
        # Cascade deletes. Django emulates the behavior of the SQL constraint
        # ON DELETE CASCADE and also deletes the object containing the
        # ForeignKey.
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    start_datetime = models.DateTimeField(
        default=datetime.now,
        verbose_name='Start Date & Time',
    )
    end_datetime = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='End Date & Time',
    )
    total_budget = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        help_text='Minimum $25',
        # validators will not be run automatically when you save a model,
        # but if you are using a ModelForm, it will run your validators on
        # any fields that are included in your form.
        validators=[MinValueValidator(25)],
    )
    daily_budget = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        help_text='Minimum $25',
        validators=[MinValueValidator(25)],
    )
    bid = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        help_text='Minimum $0.01',
        validators=[MinValueValidator(0.01)],
    )
    # Делаем упрощённо их просто свободными через запятую
    geo_position = models.TextField(
        max_length=200,
        verbose_name='GEO-position',
        blank=True,
        null=True,
    )
    categories = models.TextField(
        max_length=200,
        blank=True,
        null=True,
    )
    device_types = models.TextField(
        max_length=200,
        blank=True,
        null=True,
    )
    ACTIVE = 'AC'
    PAUSED = 'PA'
    DELETED = 'DE'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PAUSED, 'Paused'),
        (DELETED, 'Deleted'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PAUSED,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["update_date"]

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular campaign instance.
        """
        return reverse('strategy-detail', args=[str(self.id)])


class Creative(models.Model):
    """
    Model representing a creative.
    """
    campaign = models.ForeignKey(
        Campaign,
        # Cascade deletes. Django emulates the behavior of the SQL constraint
        # ON DELETE CASCADE and also deletes the object containing the
        # ForeignKey.
        on_delete=models.CASCADE
    )
    strategies = models.ManyToManyField(
        Strategy,
        # Чё-то он ругается на этот on delete у many to many
        # Ну посмотрим как дальше себя поведёт
        # on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=200)
    target_url = models.URLField(
        max_length=200,
        verbose_name='Target URL',
    )
    REWARDED = 'RE'
    INTERSTITIAL = 'IN'
    INVENTORY_TYPE_CHOICES = (
        (REWARDED, 'Rewarded video'),
        (INTERSTITIAL, 'Interstitial video'),
    )
    inventory_type = models.CharField(
        max_length=2,
        choices=INVENTORY_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    # Like a PositiveIntegerField, but only allows values under a certain
    # (database-dependent) point. Values from 0 to 32767 are safe in all
    # databases supported by Django.
    skip_sec = models.PositiveSmallIntegerField(
        default=5,
        blank=True,
        null=True,
    )
    ACTIVE = 'AC'
    PAUSED = 'PA'
    DELETED = 'DE'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PAUSED, 'Paused'),
        (DELETED, 'Deleted'),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=PAUSED,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["update_date"]

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

    def get_absolute_url(self):
        """
        Returns the url to access a particular campaign instance.
        """
        return reverse('creative-detail', args=[str(self.id)])
