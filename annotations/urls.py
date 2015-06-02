from django.conf.urls import patterns, url
from annotations import views


urlpatterns = patterns('',
    url(r'^demo/$', views.demo),
    url(r'^document/(?P<doc_id>[0-9]+)$', views.Document.as_view()), # document view
    #url(r'^document/(?P<doc_id>[0-9]+)/ngrams/(?P<ngram_id>[0-9]+)$', views.DocumentNgram.as_view()),  # actions on ngram from a document
    url(r'^lists/(?P<list_id>[0-9]+)$', views.NgramList.as_view()), # actions on list filtered by document
    url(r'^lists/(?P<list_id>[0-9]+)/ngrams(?:/(?P<ngram_id>[0-9]+))?$', views.Ngram.as_view()), # actions on ngram from a list optionally filtered by document
)
