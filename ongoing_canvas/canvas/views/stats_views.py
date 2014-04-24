import string
from collections import defaultdict

from django.conf import settings
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q, Count

from ongoing_canvas.canvas.models import FeelingData, Feeling
from ongoing_canvas.canvas.form_generator.form_generator import *
from ongoing_canvas.canvas.form_generator.placement_strategy import GridPlacementStrategy

form_generator = FormGenerator("ongoing_canvas/canvas/form_data/colors.json", "ongoing_canvas/canvas/form_data/shapes.json", GridPlacementStrategy(settings.CANVAS_HEIGHT, settings.CANVAS_WIDTH, settings.SHAPE_HEIGHT, settings.SHAPE_WIDTH, depth=1))

class AJAXStatisticsView(View):
	def get_data(self):
		return '{ "girl": "dayum!" }'

	def get(self, request, *args, **kwargs):
		response = HttpResponse(content_type="application/json")
		response.write(json.dumps(self.get_data(**kwargs)))

		return response

class Moods(AJAXStatisticsView):
	def get_data(self, **kwargs):
		if 'end' not in kwargs:
			return "{}"

		end = kwargs['end']

		if end == "top":
			order_by = '-fd_count'
		elif end == "bottom":
			order_by = 'fd_count'
		else:
			return "{}"

		annotated_feelings = [(annotated_feeling, annotated_feeling.fd_count) for annotated_feeling in Feeling.objects.annotate(fd_count=Count('feelingdata')).order_by(order_by)[:10] if annotated_feeling.fd_count > 0]

		if end == "bottom":
			annotated_feelings.reverse()

		feeling_colours = []

		for annotated_feeling in annotated_feelings:
			tupleOrNone = form_generator.get_feeling_coordinates(annotated_feeling[0].name)
			if tupleOrNone:
				(current_group_name, subgroup_index) = tupleOrNone
				colour = FormGenerator.get_colour(form_generator.settings["Coloring schemes"][current_group_name][subgroup_index], in_hsl=True)

				feeling_colours.append(colour)

		data = {
			"feelingCounts": [t[1] for t in annotated_feelings],
			"feelingLegend": [string.capitalize(t[0].name) for t in annotated_feelings],
			"feelingColours": feeling_colours
		}
		return data

class Categories(AJAXStatisticsView):
	def get_data(self, **kwargs):
		annotated_feelings = [(annotated_feeling, annotated_feeling.fd_count) for annotated_feeling in Feeling.objects.annotate(fd_count=Count('feelingdata')).order_by('-fd_count') if annotated_feeling.fd_count > 0]
		categoryCounts = defaultdict(int)
		for annotated_feeling in annotated_feelings:
			tupleOrNone = form_generator.get_feeling_coordinates(annotated_feeling[0].name)
			if tupleOrNone:
				categoryCounts[tupleOrNone[0]] += annotated_feeling[1]
		categoryCounts = categoryCounts.items()

		data = {
			"categoryCounts": [t[1] for t in categoryCounts],
			"categoryLegend": [t[0] for t in categoryCounts],
		}
		return data

