from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView,ListView

from canvas.models import FeelingData

urlpatterns = patterns('canvas.views',
	url(r'^$', TemplateView.as_view(template_name="canvas/canvas.html")),
	url(r'^feelings$', ListView.as_view(template_name="canvas/feelings.html", model=FeelingData)),
)
