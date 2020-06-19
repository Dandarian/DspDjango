from django.shortcuts import render
from .models import Campaign, Strategy, Creative
from django.views import generic

# Create your views here.


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


class CampaignListView(generic.ListView):
    model = Campaign
    paginate_by = 5


class CampaignDetailView(generic.DetailView):
    model = Campaign


class StrategyListView(generic.ListView):
    model = Strategy
    paginate_by = 5


class StrategyDetailView(generic.DetailView):
    model = Strategy


class CreativeListView(generic.ListView):
    model = Creative
    paginate_by = 5


class CreativeDetailView(generic.DetailView):
    model = Creative
