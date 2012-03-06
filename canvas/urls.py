from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView,DetailView

from canvas.models import FeelingData
from canvas.views import *

urlpatterns = patterns('canvas.views',
	url(r'^$', CanvasView.as_view()),
	url(r'^feeling/(?P<pk>\d+)/', FeelingDataDetailView.as_view()),
	url(r'^feelings$', ListView.as_view(template_name="canvas/feelings.html", model=FeelingData)),
)
