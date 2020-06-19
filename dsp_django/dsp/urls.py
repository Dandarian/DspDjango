from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^campaigns/$', views.CampaignListView.as_view(), name='campaigns'),
    url(r'^campaign/(?P<pk>\d+)$',
        views.CampaignDetailView.as_view(), name='campaign-detail'),
    url(r'^strategies/$', views.StrategyListView.as_view(), name='strategies'),
    url(r'^strategy/(?P<pk>\d+)$',
        views.StrategyDetailView.as_view(), name='strategy-detail'),
    url(r'^creatives/$', views.CreativeListView.as_view(), name='creatives'),
    url(r'^creative/(?P<pk>\d+)$',
        views.CreativeDetailView.as_view(), name='creative-detail'),
]
