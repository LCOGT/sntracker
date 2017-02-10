from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.flatpages import views

from observe.views import SupernovaView, SupernovaSchedule, ObservationView, home
from observe.models import Supernova


urlpatterns = [
    url(r'^$', home , name='home'),
    url(r'^about/$', views.flatpage, {'url': '/about/'}, name='about'),
    url(r'^education/$', views.flatpage, {'url': '/education/'}, name='education'),
    url(r'^supernova/(?P<pk>[0-9]+)/$', SupernovaView.as_view(), name='supernova_detail'),
    url(r'^supernova/(?P<pk>[0-9]+)/submit/$', SupernovaSchedule.as_view(), name='supernova_schedule'),
    url(r'^observation/(?P<pk>[0-9]+)/$', ObservationView.as_view(), name='request_detail'),
    url(r'^admin/', admin.site.urls),
]
