from django.conf.urls import patterns, include, url

base64_pattern = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'
urlpatterns = patterns('',
    url(r'^signup/', 'account.views.signup', name='signup'),
    url(r'^login/', 'account.views.user_login', name='login'),
    url(r'^logout/', 'account.views.user_logout', name='logout'),
    url(r'^profile/(?P<user_id>\d+)/$', 'account.views.show_user', name='profile'),
    url(r'^edit/$', 'account.views.edit_profile', name='edit'),
    url(r'^request_check/$', 'account.views.request_check', name='request_check'),
    url(r'^check/(?P<user_id>\d+)/$', 'account.views.check', name='check'),
    url(r'^check/(?P<user_id>\d+)/(?P<token>{})'.format(base64_pattern), 'account.views.check', name='check'),
    url(r'^reset_password/(?P<user_id>\d+)/$', 'account.views.reset_password', name='reset_password'),
    url(r'^reset_password/(?P<user_id>\d+)/(?P<token>{})'.format(base64_pattern), 'account.views.reset_password', name='reset_password'),
    url(r'^forget_password/$', 'account.views.forget_password', name='forget_password'),
    url(r'^msg_center/$', 'account.views.message_center', name="msg_center"),
    url(r'^send_msg/(?P<receiver_id>\d+)/$', 'account.views.send_message', name='send_msg'),
    url(r'^view_msg/(?P<user_id>\d+)/(?P<msg_id>\d+)/$', 'account.views.view_message', name='view_msg'),
    )
