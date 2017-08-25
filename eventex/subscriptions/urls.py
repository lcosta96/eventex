from django.conf.urls import url
from eventex.subscriptions.views import subscribe, detail


urlpatterns = [
    url(r'^$', subscribe, name='new'),
    url(r'^(\d+)/$', detail, name='detail'),
]