from django.conf.urls import patterns, url
from django.views.generic import ListView,DetailView

from ongoing_canvas.canvas.models import FeelingData
from ongoing_canvas.canvas.views.basic_views import *
from ongoing_canvas.canvas.views.stats_views import *

urlpatterns = patterns('ongoing_canvas.canvas.views.basic_views',
	url(r'^$', CanvasView.as_view(), name="canvas"),
	url(r'^snapshot/$', SnapshotView.as_view()),
	url(r'^refresh/$', 'broadcast'),
	url(r'^statistics/$', 'statistics', name="statistics"),
	url(r'^playground/$', PlaygroundView.as_view(), name="playground"),	
	url(r'^feeling/(?P<pk>\d+)/', FeelingDataDetailView.as_view()),
	url(r'^feelings$', ListView.as_view(template_name="canvas/feelings.html", model=FeelingData)),
)

urlpatterns += patterns('ongoing_canvas.canvas.views.stats_views',
	url(r'^statistics/ajax$', AJAXStatisticsView.as_view(), name="statistics_ajax"),
	url(r'^statistics/moods/(?P<end>\w+)/?$', Moods.as_view(), name="statistics_topmoods")
)

