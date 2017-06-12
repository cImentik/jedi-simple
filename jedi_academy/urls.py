from django.conf.urls import url, include

from .views import IndexView
from .views import JediChoice, JediPadawans, JediGo
from .views import CandidateCreate, CandidateDetail, CandidateExam

from .views import JediListView, JediListViewActive

jedi_urls = [
    url(r'list$', JediListView.as_view(), name='list_all'),
    url(r'active$', JediListViewActive.as_view(), name='list_active'),
    url(r'(?P<pk>[0-9]+)/padawans/$', JediPadawans.as_view(), name='padawans'),
    url(r'(?P<pk>[0-9]+)/go/(?P<cand_pk>[0-9]+)$', JediGo.as_view(), name='go'),
    url(r'^$', JediChoice.as_view(), name='choice'),
]

candidate_urls = [
    url(r'create/$', CandidateCreate.as_view(), name='create'),
    url(r'(?P<pk>[0-9]+)/$', CandidateDetail.as_view(), name='detail'),
    url(r'(?P<pk>[0-9]+)/exam/$', CandidateExam.as_view(), name='exam'),
]

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^jedi/', include(jedi_urls, namespace='jedi')),
    url(r'^candidate/', include(candidate_urls, namespace='candidate')),
]