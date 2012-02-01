from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('canvas.views',
	url(r'^$', TemplateView.as_view(template_name="canvas/canvas.html")),
)
