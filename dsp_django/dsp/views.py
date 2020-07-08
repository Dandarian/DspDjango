from django.shortcuts import render
from .models import Campaign, Strategy, Creative
# from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
# import datetime
# from django import forms
from .forms import CreateCreativeForm, CreateStrategyModelForm, CampaignForm, \
    UpdateStrategyModelForm, CreateCreativeChooseCampaignForm

# Create your views here.


@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Количество активных кампаний
    num_active_campaigns = Campaign.objects.filter(status__exact='AC').count()
    # Здесь может быть статистика, но в демо варианте только это
    return render(
        request,
        'index.html',
        context={'num_active_campaigns': num_active_campaigns},
    )


class CampaignListView(LoginRequiredMixin, generic.ListView):
    model = Campaign
    paginate_by = 5
    # ordering = ['update_date']

    # Чтобы показывать только сущности текущего пользователя.
    def get_queryset(self):
        return Campaign.objects.filter(user_id=self.request.user).order_by(
            '-update_date')


class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign

    # Это так мы прогружаем список стратегий для данной кампании
    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        strategies = Strategy.objects.filter(
            user_id=self.request.user).filter(
            campaign=self.kwargs.get('pk')).order_by('-update_date')
        context['strategies'] = strategies
        # Потом так же прогружаем список креативов
        creatives = Creative.objects.filter(
            user_id=self.request.user).filter(
            campaign=self.kwargs.get('pk')).order_by('-update_date')
        context['creatives'] = creatives
        return context

    # extra_context = {'campaign_strategy_list': campaign_strategy_list()}


class StrategyListView(LoginRequiredMixin, generic.ListView):
    model = Strategy
    paginate_by = 5

    def get_queryset(self):
        return Strategy.objects.filter(user_id=self.request.user).order_by(
            '-update_date')

    def get_queryset_for_campaign(self, campaign_id):
        return Strategy.objects.filter(user_id=self.request.user).filter(
            campaign=campaign_id).order_by('-update_date')


class StrategyDetailView(LoginRequiredMixin, generic.DetailView):
    model = Strategy

    def get_context_data(self, **kwargs):
        context = super(StrategyDetailView, self).get_context_data(**kwargs)
        creatives = Creative.objects.filter(
            user_id=self.request.user).filter(
            strategies=self.kwargs.get('pk')).order_by('-update_date')
        context['creatives'] = creatives
        return context


class CreativeListView(LoginRequiredMixin, generic.ListView):
    model = Creative
    paginate_by = 5

    def get_queryset(self):
        return Creative.objects.filter(user_id=self.request.user).order_by(
            '-update_date')


class CreativeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Creative


class CampaignCreate(LoginRequiredMixin, CreateView):
    form_class = CampaignForm
    model = Campaign
    # fields = '__all__'
    success_url = reverse_lazy('campaigns')
    # initial = {'user_id': self.request.user, }

    # Переопределяем метод form_valid() для добавления пользователя:
    # (выше указав form_class)
    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(CampaignCreate, self).form_valid(form)


class CampaignUpdate(LoginRequiredMixin, UpdateView):
    model = Campaign
    fields = ['name', 'start_datetime', 'end_datetime', 'total_budget',
              'daily_budget', 'status']
    success_url = reverse_lazy('campaigns')


class CampaignDelete(LoginRequiredMixin, DeleteView):
    model = Campaign
    # Возвращает в список
    success_url = reverse_lazy('campaigns')


@login_required
def create_strategy(request):
    """
    View function for creating a strategy
    """
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data
        # from the request (binding):
        form = CreateStrategyModelForm(request.POST)
        form.user_campaign(request.user)
        # Check if the form is valid:
        if form.is_valid():
            strategy = Strategy(
                campaign=form.cleaned_data['campaign'],
                name=form.cleaned_data['name'],
                start_datetime=form.cleaned_data['start_datetime'],
                end_datetime=form.cleaned_data['end_datetime'],
                total_budget=form.cleaned_data['total_budget'],
                daily_budget=form.cleaned_data['daily_budget'],
                bid=form.cleaned_data['bid'],
                geo_position=form.cleaned_data['geo_position'],
                categories=form.cleaned_data['categories'],
                device_types=form.cleaned_data['device_types'],
                status=form.cleaned_data['status'],
                user_id=request.user,
            )
            strategy.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('strategies'))
    # If this is a GET (or any other method) create the default form.
    else:
        form = CreateStrategyModelForm()
        form.user_campaign(request.user)
    return render(request, 'dsp/create_strategy.html', {'form': form})


"""
def update_strategy(request, pk):
    '''
    View function for updating a strategy
    '''
    strategy = get_object_or_404(Strategy, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data
        # from the request (binding):
        form = UpdateStrategyModelForm(request.POST)
        # form.user_campaign(request.user)
        # Check if the form is valid:
        if form.is_valid():
            strategy = Strategy(
                campaign=strategy.campaign,
                name=form.cleaned_data['name'],
                start_datetime=form.cleaned_data['start_datetime'],
                end_datetime=form.cleaned_data['end_datetime'],
                total_budget=form.cleaned_data['total_budget'],
                daily_budget=form.cleaned_data['daily_budget'],
                bid=form.cleaned_data['bid'],
                geo_position=form.cleaned_data['geo_position'],
                categories=form.cleaned_data['categories'],
                device_types=form.cleaned_data['device_types'],
                status=form.cleaned_data['status'],
                user_id=request.user,
            )
            strategy.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('strategies'))
    # If this is a GET (or any other method) create the default form.
    else:
        form = UpdateStrategyModelForm(
            initial={
                # 'campaign': strategy.campaign,
                'name': strategy.name,
                'start_datetime': strategy.start_datetime,
                'end_datetime': strategy.end_datetime,
                'total_budget': strategy.total_budget,
                'daily_budget': strategy.daily_budget,
                'bid': strategy.bid,
                'geo_position': strategy.geo_position,
                'categories': strategy.categories,
                'device_types': strategy.device_types,
                'status': strategy.status,
            }
        )
        # form.user_campaign(request.user)
    return render(request, 'dsp/update_strategy.html', {'form': form})
"""


class StrategyUpdate(LoginRequiredMixin, UpdateView):
    form_class = UpdateStrategyModelForm
    model = Strategy
    # template_name = 'dsp/templates/dsp/update_strategy.html'
    # fields = ['name', 'start_datetime', 'end_datetime', 'total_budget',
              # 'daily_budget', 'status'] # noqa
    success_url = reverse_lazy('strategies')


class StrategyDelete(LoginRequiredMixin, DeleteView):
    model = Strategy
    # Возвращает в список
    success_url = reverse_lazy('strategies')


@login_required
def create_creative(request):
    """
    View function for creating a creative
    """

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        print(request.POST)
        campaign_post = request.POST['campaign'] if request.POST['campaign'] \
            else False
        campaign_name = request.POST.get('campaign_name', False)
        print(campaign_post)
        if campaign_post.isdigit():
            # Create a form instance and populate it with
            # data from the request (binding):
            campaign_id = campaign_post

        if campaign_name:
            form = CreateCreativeForm(request.POST)
            form.id_campaign(campaign_id)
            form.user_strategies(request.user, campaign_id)
            # Check if the form is valid:
            if form.is_valid():
                print('valid')
                print(form.cleaned_data['strategies'])
                creative = Creative(
                    campaign=Campaign.objects.get(id=campaign_id),
                    name=form.cleaned_data['name'],
                    target_url=form.cleaned_data['target_url'],
                    inventory_type=form.cleaned_data['inventory_type'],
                    skip_sec=form.cleaned_data['skip_sec'],
                    status=form.cleaned_data['status'],
                    user_id=request.user,
                    # creation_date=form.cleaned_data['creation_date'],
                    # update_date=form.cleaned_data['update_date'],
                )
                creative.save()
                # Это нужно использовать, т. к. ManyToMany нельзя напрямую
                # сохранить
                # Также нужно сохранить до этого, т к нужен айди креатива
                creative.strategies.set(form.cleaned_data['strategies'])
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('creatives'))

        print(Campaign.objects.get(id=campaign_id))
        form = CreateCreativeForm(
            initial={'campaign': campaign_id,
                     'campaign_name': Campaign.objects.get(id=campaign_id)}
        )
        form.id_campaign(campaign_id)
        print(request.POST['campaign'])
        # print(request.POST['name'])
        # form.user_campaign(request.user)
        form.user_strategies(request.user, campaign_id)
        print('pochemy')

        # Check if the form is valid:
        if form.is_valid():
            print('valid')
            creative = Creative(
                campaign=campaign_id,
                # strategies=form.cleaned_data['strategies'],
                name=form.cleaned_data['name'],
                target_url=form.cleaned_data['target_url'],
                inventory_type=form.cleaned_data['inventory_type'],
                skip_sec=form.cleaned_data['skip_sec'],
                status=form.cleaned_data['status'],
                user_id=request.user,
                # creation_date=form.cleaned_data['creation_date'],
                # update_date=form.cleaned_data['update_date'],
            )
            creative.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('creatives'))
        # else:
        #     # Create a form instance and populate it with
        #     # data from the request (binding):
        #     form = CreateCreativeForm(request.POST)
        #     print(request.POST)
        #     print(request.POST['campaign'])
        #     # print(request.POST['name'])
        #     # form.user_campaign(request.user)
        #     form.user_strategies(request.user)

        #     # Check if the form is valid:
        #     if form.is_valid():
        #         creative = Creative(
        #             campaign=campaign_id,
        #             # strategies=form.cleaned_data['strategies'],
        #             name=form.cleaned_data['name'],
        #             target_url=form.cleaned_data['target_url'],
        #             inventory_type=form.cleaned_data['inventory_type'],
        #             skip_sec=form.cleaned_data['skip_sec'],
        #             status=form.cleaned_data['status'],
        #             user_id=request.user,
        #             # creation_date=form.cleaned_data['creation_date'],
        #             # update_date=form.cleaned_data['update_date'],
        #         )
        #         creative.save()
        #         # redirect to a new URL:
        #         return HttpResponseRedirect(reverse('creatives'))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CreateCreativeChooseCampaignForm()
        # form = CreateCreativeForm()
        # Переопределяем поле кампании, чтобы оно выдавало
        # только кампании текущего пользователя
        # т к в forms нет доступа к request
        # (костыль конечно)
        # объект не может вызвать сам себя, не создав себя
        # form.fields['campaign'] = forms.ModelChoiceField(
        #     queryset=Campaign.objects.all().filter(user_id=request.user))
        form.user_campaign(request.user)
        # Так же со стратегиями
        # form.fields['strategies'] = forms.ModelMultipleChoiceField(
        #     queryset=Strategy.objects.all().filter(user_id=request.user))
        # form.user_strategies(request.user)
        return render(request, 'dsp/create_creative_choose_campaign.html',
                      {'form': form})

    return render(request, 'dsp/create_creative.html', {'form': form})


@login_required
def update_creative(request, pk):
    """
    View function for updating a creative
    """
    creative = get_object_or_404(Creative, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # print(request.POST)
        campaign_post = request.POST['campaign'] if request.POST['campaign'] \
            else False
        campaign_name = request.POST.get('campaign_name', False)
        # print(campaign_post)
        if campaign_post.isdigit():
            campaign_id = campaign_post

        if campaign_name:
            form = CreateCreativeForm(request.POST)
            form.id_campaign(campaign_id)
            form.user_strategies(request.user, campaign_id)
            # Check if the form is valid:
            if form.is_valid():
                print('valid')
                print(form.cleaned_data['strategies'])
                creative.campaign = Campaign.objects.get(id=campaign_id)
                creative.name = form.cleaned_data['name']
                creative.target_url = form.cleaned_data['target_url']
                creative.inventory_type = form.cleaned_data['inventory_type']
                creative.skip_sec = form.cleaned_data['skip_sec']
                creative.status = form.cleaned_data['status']
                creative.user_id = request.user
                creative.save()
                # Это нужно использовать, т. к. ManyToMany нельзя напрямую
                # сохранить
                # Также нужно сохранить до этого, т к нужен айди креатива
                creative.strategies.set(form.cleaned_data['strategies'])
                # redirect to a new URL:
                return HttpResponseRedirect(reverse('creatives'))

        # form = CreateCreativeForm(
        #     initial={'campaign': campaign_id,
        #              'campaign_name': Campaign.objects.get(id=campaign_id)}
        # )
        # form.id_campaign(campaign_id)
        # form.user_strategies(request.user, campaign_id)

        # if form.is_valid():
        #     print('valid')
        #     creative = Creative(
        #         campaign=campaign_id,
        #         name=form.cleaned_data['name'],
        #         target_url=form.cleaned_data['target_url'],
        #         inventory_type=form.cleaned_data['inventory_type'],
        #         skip_sec=form.cleaned_data['skip_sec'],
        #         status=form.cleaned_data['status'],
        #         user_id=request.user,
        #     )
        #     creative.save()
        #     return HttpResponseRedirect(reverse('creatives'))

    # If this is a GET (or any other method) create the default form.
    else:
        print(creative.campaign)
        print(creative.campaign.id)
        print(creative.strategies.all())
        print(creative.strategies.all()[0])
        print(creative)
        print(creative.id)
        print(Creative.objects.get(
            id=creative.id))
        form = CreateCreativeForm(
            initial={'campaign': creative.campaign.id,
                     'campaign_name': Campaign.objects.get(
                         id=creative.campaign.id),
                     'strategies': creative.strategies.all(),
                     'name': creative.name,
                     'target_url': creative.target_url,
                     'inventory_type': creative.inventory_type,
                     'skip_sec': creative.skip_sec,
                     'status': creative.status,
                     'user_id': request.user, }
        )
        form.id_campaign(creative.campaign.id)
        form.user_strategies(request.user, creative.campaign.id)

    return render(request, 'dsp/create_creative.html', {'form': form})


class CreativeDelete(LoginRequiredMixin, DeleteView):
    model = Creative
    # Возвращает в список
    success_url = reverse_lazy('creatives')
