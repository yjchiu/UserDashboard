from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^register$', views.new),
    url(r'^login$', views.login),
    url(r'^login_process$', views.login_process),
    url(r'^dashboard/admin$', views.dashboard_admin),
    url(r'^users/new$', views.add),
    url(r'^dashboard$', views.dashboard),
    url(r'^users/show/(?P<user_id>\d+)$', views.show),
    url(r'^message_process/(?P<user_id>\d+)/(?P<active_user_id>\d+)$', views.message_process),
    url(r'^comment_process/(?P<message_id>\d+)/(?P<user_id>\d+)/(?P<active_user_id>\d+)$', views.comment_process),
    url(r'^users/edit/(?P<user_id>\d+)$', views.admin_edit),
    url(r'^users/edit$', views.edit),
    url(r'^update_info/(?P<user_id>\d+)$', views.update_info),
    url(r'^update_pwd/(?P<user_id>\d+)$', views.update_pwd),
    url(r'^update_description/(?P<user_id>\d+)$', views.update_description),
    url(r'^users/destroy/(?P<user_id>\d+)$', views.destroy),
    url(r'^logoff$', views.logoff),
]