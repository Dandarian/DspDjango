from django import forms
from .models import Campaign, Strategy
from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError
# from django.utils.translation import ugettext_lazy as _
# import datetime #for checking renewal date range.


class CreateStrategyModelForm(forms.ModelForm):
    class Meta:
        model = Strategy
        exclude = ['user_id', 'creation_date', 'update_date']
        # widgets = {
        #     'start_datetime': forms.SplitDateTimeWidget,
        #     'end_datetime': forms.SplitDateTimeWidget,
        # }

    def user_campaign(self, user):
        self.fields['campaign'] = forms.ModelChoiceField(
            queryset=Campaign.objects.all().filter(user_id=user))


class UpdateStrategyModelForm(forms.ModelForm):
    class Meta:
        model = Strategy
        exclude = ['campaign', 'user_id', 'creation_date', 'update_date']
        # widgets = {
        #     'start_datetime': forms.SplitDateTimeWidget,
        #     'end_datetime': forms.SplitDateTimeWidget,
        # }


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        exclude = ('user_id',)


class CreateCreativeChooseCampaignForm(forms.Form):
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.all())

    # по идее эти методы можно спрятать в ининт
    # но это как-то не оч на мой взгляд
    def user_campaign(self, user):
        self.fields['campaign'] = forms.ModelChoiceField(
            queryset=Campaign.objects.all().filter(user_id=user))


class CreateCreativeForm(forms.Form):
    # Переопределяем метод инит, чтобы review могло отдавать значение юзера
    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    campaign = forms.ModelChoiceField(
        queryset=Campaign.objects.all(),
        label='Campaign id')
    campaign_name = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    strategies = forms.ModelMultipleChoiceField(
        queryset=Strategy.objects.all())

    # по идее эти методы можно спрятать в ининт
    # но это как-то не оч на мой взгляд

    def id_campaign(self, id):
        self.fields['campaign'] = forms.ModelChoiceField(
            queryset=Campaign.objects.all().filter(id=id),
            widget=forms.TextInput(attrs={'readonly': 'readonly'}),
            label='Campaign id')

    def user_strategies(self, user, campaign_id):
        self.fields['strategies'] = forms.ModelMultipleChoiceField(
            queryset=Strategy.objects.all().filter(
                user_id=user).filter(campaign=campaign_id))

    name = forms.CharField()
    target_url = forms.URLField(
        label='Target URL',
    )
    REWARDED = 'RE'
    INTERSTITIAL = 'IN'
    INVENTORY_TYPE_CHOICES = (
        (REWARDED, 'Rewarded video'),
        (INTERSTITIAL, 'Interstitial video'),
    )
    inventory_type = forms.ChoiceField(
        choices=INVENTORY_TYPE_CHOICES,
    )
    # Like a PositiveIntegerField, but only allows values under a certain
    # (database-dependent) point. Values from 0 to 32767 are safe in all
    # databases supported by Django.
    skip_sec = forms.IntegerField()
    ACTIVE = 'AC'
    PAUSED = 'PA'
    DELETED = 'DE'
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (PAUSED, 'Paused'),
        (DELETED, 'Deleted'),
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
    )
    # user_id = forms.ModelChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.HiddenInput(),
    # )

    # creation_date = forms.DateTimeField()
    # update_date = forms.DateTimeField()
