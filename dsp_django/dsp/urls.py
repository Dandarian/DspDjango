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
    url(r'^campaign/create/$', views.CampaignCreate.as_view(),
        name='campaign-create'),
    url(r'^campaign/(?P<pk>\d+)/update/$', views.CampaignUpdate.as_view(),
        name='campaign-update'),
    url(r'^campaign/(?P<pk>\d+)/delete/$', views.CampaignDelete.as_view(),
        name='campaign-delete'),
    url(r'^strategy/create/$', views.create_strategy, name='strategy-create'),
    url(r'^strategy/(?P<pk>\d+)/update/$', views.StrategyUpdate.as_view(),
        name='strategy-update'),
    url(r'^strategy/(?P<pk>\d+)/delete/$', views.StrategyDelete.as_view(),
        name='strategy-delete'),
    url(r'^creative/create/$', views.create_creative, name='creative-create'),
    url(r'^creative/(?P<pk>\d+)/update/$', views.update_creative, name='creative-update'),
]
