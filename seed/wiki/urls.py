from django.conf.urls import patterns, include, url

from wiki import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^form/$', views.showform, name='showform'),
    url(r'^show/(?P<entry_id>\d+)/$', views.get_entry, name='show'),
    url(r'^show/(?P<entry_id>\d+)/(?P<ver_id>\d+)/$', views.get_entry, name='show'),
    url(r'^versions/(?P<entry_id>\d+)/$', views.versions_entry, name='versions'),
    url(r'^edit/(?P<entry_id>\d+)/$', views.edit_entry, name='edit'),
    url(r'^edit/$', views.edit_entry, name='edit'),
    url(r'^entry/(?P<entry_id>\d+)/history/(?P<ver_id>\d+)/$',views.revert_entry, name='revert_entry'),
    url(r'^search_suggest/$', views.search_suggest, name='search_suggest'),
    url(r'^suggest_tag/$', views.suggest_tag, name='suggest_tag'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_by_tag/$', views.search_by_tag, name='search_by_tag'),
    url(r'^search_tag/$', views.search_tag, name='search_tag'),
    url(r'^suggest_link/$', views.suggest_link, name='suggest_link'),
    url(r'^vote_up/(?P<entry_id>\d+)/$', views.vote_up, name="vote_up"),
    url(r'^vote_down/(?P<entry_id>\d+)/$', views.vote_down, name="vote_down"),
    url(r'^add_tag/(?P<entry_id>\d+)/$', views.add_tag, name='add_tag'),
    url(r'^remove_tag/(?P<entry_id>\d+)/$', views.remove_tag, name='remove_tag'),
    url(r'^upload/(?P<entry_id>\d+)/$', views.upload_attach, name='upload'),
    url(r'^delete/(?P<entry_id>\d+)/$', views.delete_attach, name='delete'),
    url(r'^delete_entry/(?P<entry_id>\d+)/$', views.delete_entry, name='delete_entry'),

)
